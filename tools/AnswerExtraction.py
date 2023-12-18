from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# TODO: these models start downloading once they're used. perhaps better to download them once you create the container.

def entity_answer_extraction(question, context):
    if context == '':
        return 'No answer from LLM'

    model_name = "/sharedFolder/models/entity_answer_extraction_model"
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': question,
        'context': context
    }
    res = nlp(QA_input)
    return res

def boolean_answer_extraction(question, context):
    if context == '':
        return 'No answer from LLM'
    model = AutoModelForSequenceClassification.from_pretrained("models/boolean_answer_extraction_model")
    tokenizer = AutoTokenizer.from_pretrained("models/boolean_answer_extraction_model")

    encoded_input = tokenizer([(question, context)], padding=True, truncation=True, return_tensors="pt")

    with torch.no_grad():
        model_output = model(**encoded_input)
        probabilities = torch.softmax(model_output.logits, dim=-1).cpu().tolist()

    probability_no = [round(prob[0], 2) for prob in probabilities]
    probability_yes = [round(prob[1], 2) for prob in probabilities]

    return (probability_yes, probability_no)

def extract_entity(ans, entities):
    for ent in entities:
        if str(ent['name']) in ans:
            return ent