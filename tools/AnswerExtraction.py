from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
def answer_extraction(question, context):
    model_name = "deepset/roberta-base-squad2"

    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': question,
        'context': context
    }
    res = nlp(QA_input)
    return res


if __name__ == "__main__":
    q = 'Is Rome the capital of Italy?'
    a = 'Bologne is the capital of Italy'
    print(answer_extraction(q, a))


