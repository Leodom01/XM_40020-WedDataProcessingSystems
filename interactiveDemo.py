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

    #Pre processing phase
    preProc = PreProcessor(R)
    print("Pre processed: ", preProc.pipeline())

    # Named entity recognition - temporarily using spacy
    ner = NER(raw_text=R)
    doc = ner.ner_spacy()
    # ner.spacyVisulizer(doc)

    # Open Relation extractions
    re = OpenRE()
    re_threshold = 0.7
    triples = re.extract_relations_stanford(R)
    print("Triples extracted:")
    for triple in triples:
        print(triple)
    # rel_ext.extract_relations_stanford()







