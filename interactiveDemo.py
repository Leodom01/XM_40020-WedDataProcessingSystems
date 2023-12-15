from tools.PreProcessor import PreProcessor
from tools.NER import NER
from tools.OpenRE import OpenRE
from llama_cpp import Llama
import tools.QuestionClassification as qc
import tools.AnswerExtraction as ae
from tools.EntityLinking import EntityLinker
import tools.QuestionToStatement as qts
import tools.FactChecking as fc
# LLaMA setup
model_path = "/home/user/models/llama-2-7b.Q4_K_M.gguf"
llm = Llama(model_path=model_path, verbose=False)

while True:
    R = A = C = ""
    E = []

    # Input phase
    user_question = input("Type your question:\n")

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
    # R = "Titus O’Neil Says He’ll Do Whatever NBA Asks of Him, Enjoyed Commentary"
    print("LLaMA Output: %s" % R)
    print("==========================")

    #Pre processing phase
    preProc = PreProcessor(R)
    print("Pre processed: ", preProc.pipeline())
    print("==========================")


    # Named entity recognition - temporarily using spacy
    print("Named entities:")
    ner = NER(raw_text= user_question + ". " + R )
    doc = ner.ner_spacy()
    for ent in set(doc.ents):
        print(ent)

    print("==========================")
    print("Entities link:")
    entityLinker = EntityLinker()
    entities = []
    for sent in doc.sents:
        for entity in sent.ents:
            name = entity
            link = entityLinker.run_linking(R, name)
            print(link)
            entities.append({'name': name, 'link': link})
    for entity in entities:
        print(entity["name"], " : ", entity['link'])

    print("==========================")
    print("Extracted Answer:")
    qType = qc.classify_question(user_question)
    if qc.classify_question(user_question) == 'Boolean':
        pyes, pno = ae.boolean_answer_extraction(user_question, R)
        print(f"P(yes): {pyes}")
        print(f"P(no): {pno}")
    else:
        extractedEnt = ae.entity_answer_extraction(user_question, R)
        print(f"Answer extracted:{extractedEnt}")

    print("==========================")
    print("Extracted relations:")
    # Open Relation extractions
    re = OpenRE()
    re_input = ''
    if qType == 'Boolean':
        re_input = user_question
    if qType == 'Entity':
        re_input = qts.replace_wh_word_with_entity(user_question, extractedEnt['answer'])
    if qType == 'Completion':
        re_input = user_question + extractedEnt

    re_input = re.statement_with_wikidatIDs(re_input, entities)
    print(f"Factual statement: {re_input}")
    triples = re.extract_relations_stanford(re_input)
    for triple in triples:
        print(triple)
    print("==========================")

    print(re.find_best_triple(triples))
    mainTriple = re.find_best_triple(triples)
    fact_check_res = fc.check_relationship(mainTriple['subject'], mainTriple['relation'], mainTriple['object'])

    print(fact_check_res)


    if qType == 'Boolean':
        if (pyes > pno and fact_check_res == True) or (pyes < pno and fact_check_res == False):
            print('CORRECT')
        else:
            print('INCORRECT')

    if qType == 'Entity' or qType == 'Completion':
        if fact_check_res == True:
            print('CORRECT')
        else:
            print("INCORRECT")











