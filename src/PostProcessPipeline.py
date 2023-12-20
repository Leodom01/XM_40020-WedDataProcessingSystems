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
        print("===============================================")
        print("User question:")
        qType = qc.classify_question(user_question)
        print(user_question, " | Type:", qType)
        if user_question is None:
            print("No input question provided!")
            return {'R': llm_output, 'A': '', 'C': '', 'E': []}
        print("==========================")
        print("Model answer:")
        print(llm_output)
        # Named entity recognition
        print("==========================")
        print("Named entities found:")
        ner = NER()
        doc = ner.ner_spacy(user_question +" "+ llm_output)
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
                name = entity
                try:
                    wikidataID, wikipedia_link = entityLinker.link_entity(punc_free_sent, str(name))
                except:
                    continue
                if wikipedia_link is not None:
                    entities.append({"name": name, "link": wikipedia_link, 'wikidata_ID': wikidataID})
        entities_set = set()
        for entity in entities:
            entities_set.add((entity["name"].text.lower(), entity["link"], entity['wikidata_ID']))

        for entity in entities_set:
            print(entity[0], " : ", entity[1], " - ", entity[2])
        E = entities_set
        print("==========================")
        print("Extracted Answer:")
        A = self.answerExt.extract_answer(qType, entities, user_question, llm_output)
        if A is None:
            return {'R': llm_output, 'A': '', 'C': 'incorrect', 'E': E}
        print(A)
        print("==========================")
        # Open Relation extractions
        fact_statement = qts.construct_factual_statement(qType, entities, user_question, A)
        print(f"Factual statement: {fact_statement}")
        triples = self.relation_extraction.extract_relations_stanford(fact_statement)
        print("All the triples extracted:")
        for triple in triples:
            print(triple)
        mainTriple = utils.find_suitable_triple(triples)
        print("Triple chosen for fact checking:")
        print(mainTriple)
        print("==========================")
        if qType is not 'Boolean': A = A['link']
        if mainTriple is None:
            return {'R': llm_output, 'A': A, 'C': 'incorrect', 'E': E}
        C = self.factCheck.fact_check_triple(qType, A, mainTriple)

        return {'R': llm_output, 'A': A, 'C': C, 'E': E}

if __name__ == "__main__":
    tmp = LLM_PostProcess()
    tmp.pipeline("What is the capital of Italy?", "Rome is the capital of Italy.")