from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
def entity_answer_extraction(question, context):
    if context == '':
        return 'No answer from LLM'
    model_name = "deepset/roberta-base-squad2"

    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': question,
        'context': context
    }
    res = nlp(QA_input)
    print(f"q={question},ans={context}:\n{res}")
    # return res

def boolean_answer_extraction(question, context):
    if context == '':
        return 'No answer from LLM'
    model = AutoModelForSequenceClassification.from_pretrained("nfliu/roberta-large_boolq")
    tokenizer = AutoTokenizer.from_pretrained("nfliu/roberta-large_boolq")

    encoded_input = tokenizer([(question, context)], padding=True, truncation=True, return_tensors="pt")

    with torch.no_grad():
        model_output = model(**encoded_input)
        probabilities = torch.softmax(model_output.logits, dim=-1).cpu().tolist()

    probability_no = [round(prob[0], 2) for prob in probabilities]
    probability_yes = [round(prob[1], 2) for prob in probabilities]

    print(f"q={question}|ans={context}:\nno={probability_no},yes={probability_yes}")
    # print(f"Question: {question}")
    # print(f"Context: {context}")
    # print(f"p(No | question, context): {probability_no}")
    # print(f"p(Yes | question, context): {probability_yes}")


if __name__ == "__main__":
    pass

