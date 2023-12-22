from src.PreProcessor import PreProcessor
from src.NER import NER
from src.OpenRE import OpenRE
import src.QuestionClassification as qc
import src.AnswerExtraction as ae
from src.EntityLinking import EntityLinker
import src.QuestionToStatement as qts
import src.FactChecking as fc
import src.utils as utils
"""
This module is the main pipeline to handle post-processing of the LLM output.
"""
class LLM_PostProcess:
    def __init__(self):
        self.ner = NER()
        self.preProc = PreProcessor()
        self.relation_extraction = OpenRE()
        self.answerExt = ae.AnswerExtraction()
        self.factCheck = fc.FactChecking()


    def pipeline(self, user_question, llm_output):
        """
        Calls modules to do a series of operations to post process LLM's output.

        This method executes various steps, including classification of the question type,
        printing information about the user question and model answer, named entity recognition,
        entity linking, answer extraction, construction of factual statements, open relation extraction,
        and fact checking.

        Parameters:
            user_question: str
            llm_output: str

        Returns:
        - dict: A dictionary containing the processed information with the following keys:
        - 'R' (str): LLM output.
        - 'A' (str): Extracted answer or an empty string if not found.
        - 'C' (str): Result of fact-checking, can be 'correct', 'incorrect'.
        - 'E' (list): List of linked entities.
        """
        print("===============================================")
        print("User question:")
        question_type = qc.classify_question(user_question)
        print(user_question, " | Type:", question_type)
        print("==========================")
        print("Model answer:")
        print(llm_output)
        # Named entity recognition
        print("==========================")
        print("Named entities found:")
        # entity recognition of user input and LLM output
        doc = self.ner.ner_spacy(user_question +" "+ llm_output)
        for ent in doc.ents:
            print(ent)
        # Entity Linking
        print("==========================")
        print("Linked entities:")
        entityLinker = EntityLinker()
        entities = []
        for sent in doc.sents:
            for entity in sent.ents:
                # sometimes the NER module recognizes numbers as entities
                if entity.text.isnumeric() and len(entity.text) == 1:
                    continue
                punc_free_sent = self.preProc.remove_punctuation(str(sent))
                linked_ent = entityLinker.link_entity(punc_free_sent, entity.text)
                if linked_ent is None:
                    continue
                entities.append(linked_ent)
        # removing the duplicate entities
        E = utils.remove_dup_dict(entities)
        # printing the linked entities
        for entity in E:
            print(f"{entity['name']} - {entity['link']} - {entity['wikidata_ID']}")
        print("==========================")
        print("Extracted Answer:")
        A = self.answerExt.extract_answer(question_type, E, user_question, llm_output)
        # if no answer was extracted
        if A is None:
            return {'R': llm_output, 'A': '', 'C': 'incorrect', 'E': E}
        print(A)
        print("==========================")
        # Open Relation extractions
        fact_statement = qts.construct_factual_statement(question_type, E, user_question, A)
        print(f"Factual statement: {fact_statement}")
        triples = self.relation_extraction.extract_relations_stanford(fact_statement)
        print("All the triples extracted:")
        for triple in triples:
            print(triple)
        mainTriple = utils.find_suitable_triple(triples)
        print("Triple chosen for fact checking:")
        print(mainTriple)
        print("==========================")
        if question_type != 'Boolean': A = A['link']
        # if cannot find a suitable triple, return the fact checking as incorrect
        if mainTriple is None:
            return {'R': llm_output, 'A': A, 'C': 'incorrect', 'E': E}
        C = self.factCheck.fact_check_triple(question_type, A, mainTriple)

        return {'R': llm_output, 'A': A, 'C': C, 'E': E}

if __name__ == "__main__":
    tmp = LLM_PostProcess()
    tmp.pipeline("What is the capital of Italy?", "Rome is the capital of Italy.")