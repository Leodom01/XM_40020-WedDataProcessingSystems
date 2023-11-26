import os
os.environ["NLTK_DATA"] = "/sharedFolder/nltk_data"

from ctransformers import AutoModelForCausalLM
from tools.PreProcessor import PreProcessor

# LLaMA setup
repository="TheBloke/Llama-2-7B-GGUF"
model_file="llama-2-7b.Q4_K_M.gguf"
llm = AutoModelForCausalLM.from_pretrained(repository, model_file=model_file, model_type="llama")

while True:
    R = A = C = ""
    E = []

    # Input phase
    prompt = input("Type your question:\n")
    print("Computing the answer (can take some time)...")
    #R = llm(prompt)
    # Demo answer to test quickly
    R = "Titus O’Neil Says He’ll Do Whatever WWE Asks of Him, Enjoyed Commentary"
    print("LLaMA Output: %s" % R)

    #Pre processing phase
    preProc = PreProcessor(R)
    print("Pre processed: ", preProc.pipeline())

