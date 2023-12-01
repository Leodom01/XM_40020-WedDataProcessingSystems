import os
os.environ["NLTK_DATA"] = "/sharedFolder/nltk_data"

from ctransformers import AutoModelForCausalLM
from tools.PreProcessor import PreProcessor
from tools.NER import NER
from tools.OpenRE import OpenRE
# LLaMA setup
repository="TheBloke/Llama-2-7B-GGUF"
model_file="llama-2-7b.Q4_K_M.gguf"

llm = AutoModelForCausalLM.from_pretrained(repository, model_file=model_file, model_type="llama")
# Off loading layers to gpu, install ctransformers with special commands
# llm = AutoModelForCausalLM.from_pretrained(repository, model_file=model_file, model_type="llama", gpu_layers=300)



while True:
    R = A = C = ""
    E = []

    # Input phase
    prompt = input("Type your question:\n")
    print("Computing the answer (can take some time)...")
    R = llm(prompt)
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
    rel_ext = OpenRE(R)
    rel_ext.extract_relations()





