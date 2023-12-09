from tools.PreProcessor import PreProcessor
from tools.NER import NER
from tools.OpenRE import OpenRE
from llama_cpp import Llama

# LLaMA setup
model_path = "/home/user/models/llama-2-7b.Q4_K_M.gguf"
llm = Llama(model_path=model_path, verbose=False)

while True:
    R = A = C = ""
    E = []

    # Input phase
    prompt = "Q:" + input("Type your question:\n") + " A:"
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
    ner = NER(raw_text=R)
    doc = ner.ner_spacy()
    for ent in doc.ents:
        print(ent)
    print("==========================")

    print("Extracted relations:")
    # Open Relation extractions
    re = OpenRE()
    triples = re.extract_relations_stanford(R)
    for triple in triples:
        print(triple)
    print("==========================")









