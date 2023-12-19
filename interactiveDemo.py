from llama_cpp import Llama
from tools.PostProcessPipeline import LLM_PostProcess
import pandas as pd
import tools.utils as utils
# LLaMA setup
model_path = "/home/user/models/llama-2-7b.Q4_K_M.gguf"
llm = Llama(model_path=model_path, verbose=False)

llm_postprocess = LLM_PostProcess()
# df = pd.read_csv("questions_and_plotting/questions.csv")

# def load_confusion_data():
#     data = {}
#     cnt = 0
#     for cell in df["Question"]:
#         data[f"Q{cnt}"] = {'Q': cell}
#         cnt+=1
#     print(data)
#     return data
def run_single():


    # Extract the question if input is in the following format: "Question: Q Answer:"
    user_question = utils.extract_entity(input('Type your question:'))
    prompt = 'Q:' + user_question + ' A: '
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

def run_batch():
    data = utils.load_data('task_data/example_in.txt')
    # data = load_confusion_data()
    for q in data.keys():
        # Extract the question if input is in the following format: "Question: Q Answer:"
        user_question = utils.extract_text(data[q]['Q'])
        prompt = 'Q:' + user_question + ' A: '
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
        output = llm_postprocess.pipeline(data[q]['Q'], R)
        data[q]['R'] = output['R']
        data[q]['A'] = output['A']
        data[q]['C'] = output['C']
        data[q]['E'] = output['E']
    utils.output(data, 'task_data/OUTPUT.txt')
    # df['Predicted'] = [data[x]['C'] for x in data.keys()]
    # df.to_csv("questions_and_plotting/questions.csv", index=False)
run_batch()

