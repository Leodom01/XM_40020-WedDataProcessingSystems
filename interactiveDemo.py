import sys
from llama_cpp import Llama
from src.PostProcessPipeline import LLM_PostProcess
import src.utils as utils
import src.IOHandler as IO
"""
This demo showcases the usage of the post processing pipeline
"""
# LLaMA setup
model_path = "/home/user/models/llama-2-7b.Q4_K_M.gguf"
llm = Llama(model_path=model_path, verbose=False)
def run_batch(input_path="task_data/example_input.txt", output_path="task_data/example_output.txt"):
    print("Models are being loaded...this may take up to couple of minutes...")
    data = IO.load_data(input_path)
    for question in data.keys():
        # handle cases when no question is provided
        if question is None or len(question) == 0:
            continue
        # Extract the question if input is in the following format: "Question: Q Answer:", if not use the given input
        user_question = utils.extract_text(data[question]['Q'])
        prompt = 'Q:' + user_question + ' A: '
        print("The LLM is computing the answer (can take some time)...")
        R = llm(
            prompt,  # Prompt
            max_tokens=64,  # Generate up to 64 tokens
            stop=[
                "Q:",
                "\n",
            ],  # Stop generating just before the model would generate a new question
            echo=True,  # Echo the prompt back in the output
        )["choices"][0]["text"]
        R = R[len(prompt) :]
        output = llm_postprocess.pipeline(user_question, R)
        data[question]['R'] = output['R']
        data[question]['A'] = output['A']
        data[question]['C'] = output['C']
        data[question]['E'] = output['E']
    IO.output(data, output_path)

if __name__ == "__main__":
    llm_postprocess = LLM_PostProcess()
    # Expected call: python3 inputFile.txt outputFile.txt
    if(len(sys.argv) >= 3):
        run_batch(sys.argv[1], sys.argv[2])
    else:
        run_batch()

