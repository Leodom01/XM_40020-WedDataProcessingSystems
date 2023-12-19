from llama_cpp import Llama
from tools.PostProcessPipeline import LLM_PostProcess
import pandas as pd
# LLaMA setup
model_path = "/home/user/models/llama-2-7b.Q4_K_M.gguf"
llm = Llama(model_path=model_path, verbose=False)


def write_it_also_in_csv(C,df):
    #print("received" + C)
    df["Predicted"]=C

def main_section(user_question, user_choice,df):
    if user_question == "brk":
        return  # TODO: remove this if everything works well
    prompt = "Q:" + user_question + " A:"
    print("Computing the answer (can take some time)...")
    R = llm(
        prompt,  # Prompt
        max_tokens=64,  # Generate up to 32 tokens
        stop=[
            "Q:",
            "\n",
        ],  # Stop generating just before the model would generate a new question
        echo=True,  # Echo the prompt back in the output
    )["choices"][0]["text"]
    R = R[len(prompt) :]
    output = llm_postprocess.pipeline(user_question, R)
    write_it_also_in_csv(output['C'], df)


while True:
    llm_postprocess = LLM_PostProcess()

    user_choice = input(
        "Type I to run interactive demo, any other letter to run Fixed demo:\n"
    )
    if user_choice == 'brk': break
    if user_choice == "I":
        user_question = input("Type your question:\n")
        main_section(user_question, user_choice,0)
    else:
        df = pd.read_csv("questions_and_plotting/questions.csv")
        for cell in df["Question"]:
            print("Testing question" + cell)
            main_section(cell, user_choice,df)
        df.to_csv("questions_and_plotting/questions.csv", index=False)