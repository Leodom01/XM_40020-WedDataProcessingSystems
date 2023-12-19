from tools.PreProcessor import PreProcessor
from tools.NER import NER
from tools.OpenRE import OpenRE
import tools.QuestionClassification as qc
import tools.AnswerExtraction as ae
from tools.EntityLinking import EntityLinker
import tools.QuestionToStatement as qts
import tools.FactChecking as fc
import tools.utils as utils
"""
This module is the main pipeline to handle post-processing of the LLM output.
"""
class LLM_PostProcess:
    def __init__(self):
        self.ner = NER()
        self.preProc = PreProcessor()
        self.relation_extraction = OpenRE()

    def pipeline(self, question, llm_output):
        if question is None:
            print("No input question provided!")
            return
        print("==========================")
        print("Model answer:")
        print(llm_output)
        # Extract the question if input is in the following format: "Question: Q Answer:"
        user_question = utils.extract_text(question)
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
                punc_free_sent = self.preProc.remove_punctuation(str(sent))
                name = entity
                try:
                    wikidataID, wikipedia_link = entityLinker.link_entity(punc_free_sent, str(name))
                except:
                    continue
                if wikipedia_link is not None:
                    entities.append({"name": name, "link": wikipedia_link, 'wikidata_ID': wikidataID})
        E = entities
        entities_set = set()
        for entity in entities:
            entities_set.add((entity["name"].text.lower(), entity["link"], entity['wikidata_ID']))

        for entity in entities_set:
            print(entity[0], " : ", entity[1], " - ", entity[2])

        print("==========================")
        print("Extracted Answer:")
        qType = qc.classify_question(user_question)
        A = ae.extract_answer(qType, entities, user_question, llm_output)
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
        #TODO: if main triple is null do something
        if mainTriple is None:
            return
        C = fc.fact_check_triple(qType, A, mainTriple)

        return {'R': llm_output, 'A': A, 'C': C, 'E': entities}

if __name__ == "__main__":
    tmp = LLM_PostProcess()
    tmp.pipeline("What is the capital of Italy?", "Rome is the capital of Italy.")