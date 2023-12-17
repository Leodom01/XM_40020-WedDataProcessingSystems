from tools.PreProcessor import PreProcessor
from tools.NER import NER
from tools.OpenRE import OpenRE
from llama_cpp import Llama
import tools.QuestionClassification as qc
import tools.AnswerExtraction as ae
from tools.EntityLinking import EntityLinker
import tools.QuestionToStatement as qts
import tools.FactChecking as fc
import tools.LoadTestData as ltd
import pandas as pd

# LLaMA setup
model_path = "/home/user/models/llama-2-7b.Q4_K_M.gguf"
llm = Llama(model_path=model_path, verbose=False)

re = OpenRE()

while True:
    R = A = C = ""
    E = []

    user_choice = input("Type I to run interactive demo, any other letter to run Fixed demo:\n")
    if user_choice== "I":
        user_question = input("Type your question:\n")
        main_section(user_question,user_choice)
    else: 
        df = pd.read_csv("questions.csv")
        for cell in df["Question"]:
            print("Testing question"+cell)
            main_section(cell,user_choice)
    
    def main_section(user_question,user_choice):
        if user_question == 'brk': break # TODO: remove this if everything works well
        prompt = "Q:" + user_question + " A:"
        print("Computing the answer (can take some time)...")
        R = llm(
            prompt,  # Prompt
            max_tokens=64,  # Generate up to 32 tokens
            stop=["Q:", "\n"],  # Stop generating just before the model would generate a new question
            echo=True  # Echo the prompt back in the output
        )['choices'][0]['text']
        R = R[len(prompt):]
        # Demo answer to test quickly
        # R = "Rome is the capital of Italy"
        print("LLaMA Output: %s" % R)
        print("==========================")
    
        #Pre processing phase
        preProc = PreProcessor(R)
        print("Pre processed: ", preProc.pipeline())
        print("==========================")
    
    
        # Named entity recognition - temporarily using spacy
        print("Named entities:")
        text = user_question + ". " + R
    
        ner = NER(raw_text= text)
        doc = ner.ner_spacy()
        for ent in doc.ents:
            print(ent)
    
        print("==========================")
        print("Linked entities:")
    
        entityLinker = EntityLinker()
        entities = []
        for sent in doc.sents:
            for entity in sent.ents:
                punc_free_sent = preProc.remove_punctuation(str(sent))
                name = entity
                link = entityLinker.run_linking(punc_free_sent, str(name))
                entities.append({'name': name, 'link': link})
        E = entities
        entities_set = set()
        for entity in entities:
            entities_set.add((entity["name"].lower(), entity['link']))
    
        for entity in entities_set:
            print(entity[0], " : ", entity[1])
    
        print("==========================")
        print("Extracted Answer:")
        qType = qc.classify_question(user_question)
        if qc.classify_question(user_question) == 'Boolean':
            pyes, pno = ae.boolean_answer_extraction(user_question, R)
            print(f"yes = {pyes} | no = {pno}")
            if pyes > pno :
                A = 'Yes'
            else:
                A = 'No'
        else:
            model_ans_extraction = ae.entity_answer_extraction(user_question, R)
            extracted_ent = ae.extract_entity(model_ans_extraction['answer'], entities)
            A = extracted_ent
            print(extracted_ent['name'])
    
        print("==========================")
        # Open Relation extractions
        re_input = ''
        if qType == 'Boolean':
            re_input = user_question
        if qType == 'Entity':
            re_input = qts.replace_wh_word_with_entity(user_question, str(extracted_ent['name']))
        if qType == 'Completion':
            re_input = user_question + str(extracted_ent['name'])
        print(f"Factual statement: {re_input}")
        wikiID_fact_statement = re.statement_with_wikidatIDs(re_input, entities)
        triples = re.extract_relations_stanford(wikiID_fact_statement)
        print("All the triples extracted:")
        for triple in triples:
            print(triple)
        mainTriple = re.find_best_triple(triples)
        print("Triple chosen for fact checking:")
        print(mainTriple)
        if mainTriple is None:
            continue
        fact_check_res = fc.check_relationship(mainTriple['subject'], mainTriple['relation'], mainTriple['object'])
        print("==========================")
        print("Fact check result:")
        print(fact_check_res)
        print("correct/incorrect:")
        if qType == 'Boolean':
            if (pyes > pno and fact_check_res == True) or (pyes < pno and fact_check_res == False):
                C = 'correct'
                print('CORRECT')
            else:
                C = 'incorrect'
                print('INCORRECT')
            if user_choice!="I":
                write_it_also_in_csv(C)
    
        if qType == 'Entity' or qType == 'Completion':
            if fact_check_res == True:
                C = 'correct'
                print('CORRECT')
            else:
                C = 'incorrect'
                print("INCORRECT")
            if user_choice!="I":
                write_it_also_in_csv(C)


def write_it_also_in_csv(C):
    print("received"+C)
    #write in csv
    

