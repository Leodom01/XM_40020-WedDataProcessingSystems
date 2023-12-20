from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import src.utils as utils
# TODO: these models start downloading once they're used. perhaps better to download them once you create the container.
class AnswerExtraction:

    def __init__(self):
        entity_model_name = "/sharedFolder/models/entity_answer_extraction_model"
        self.entities_answer_extractor = pipeline('question-answering',
                                                  model=entity_model_name,
                                                  tokenizer=entity_model_name)

        boolean_model_name = "/sharedFolder/models/boolean_answer_extraction_model"
        self.boolean_model_extractor = AutoModelForSequenceClassification.from_pretrained(boolean_model_name)
        self.boolean_tokenizer_extractor = AutoTokenizer.from_pretrained(boolean_model_name)

    def entity_answer_extraction(self, question, context):
        if context == '':
            return None

        QA_input = {
            'question': question,
            'context': context
        }
        res = self.entities_answer_extractor(QA_input)
        print("Entity answer extraction model: ", res['answer'])
        return res

    def boolean_answer_extraction(self, question, context):
        if context == '':
            return 'No answer from LLM'

        encoded_input = self.boolean_tokenizer_extractor([(question, context)], padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            model_output = self.boolean_model_extractor(**encoded_input)
            probabilities = torch.softmax(model_output.logits, dim=-1).cpu().tolist()

        probability_no = [round(prob[0], 2) for prob in probabilities]
        probability_yes = [round(prob[1], 2) for prob in probabilities]

        return (probability_yes, probability_no)

    def extract_answer(self, question_type, entities, question, context):
        if question_type == "Boolean":
            pyes, pno = self.boolean_answer_extraction(question, context)
            if pyes > pno:
                A = "Yes"
            else:
                A = "No"
            return A
        else:
            ext_ent = self.entity_answer_extraction(question, context)
            A = utils.extract_entity(ext_ent['answer'], entities)
            if A is None:
                return
            return A
