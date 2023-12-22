from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import src.utils as utils

class AnswerExtraction:
    """
    A class handling answer extraction methods using different models.
    """
    def __init__(self):
        entity_model_name = "/sharedFolder/models/entity_answer_extraction_model"
        self.entities_answer_extractor = pipeline('question-answering',
                                                  model=entity_model_name,
                                                  tokenizer=entity_model_name)

        boolean_model_name = "/sharedFolder/models/boolean_answer_extraction_model"
        self.boolean_model_extractor = AutoModelForSequenceClassification.from_pretrained(boolean_model_name)
        self.boolean_tokenizer_extractor = AutoTokenizer.from_pretrained(boolean_model_name)

    def entity_answer_extraction(self, question, context):
        """
        Extracts an answer using roberta_squad2.
        """
        QA_input = {
            'question': question,
            'context': context
        }
        res = self.entities_answer_extractor(QA_input)['answer']
        print("Answer extracted by roberta_squad2: ", res)
        return res

    def boolean_answer_extraction(self, question, context):
        """
        Extracts a boolean answer using roberta_large_boolq.

        Args:
        - question (str): The question user provided
        - context (str): language model's response

        Returns:
        - tuple: A tuple containing probabilities of yes and no.
        """
        if context == '':
            return 'No answer from LLM'

        encoded_input = self.boolean_tokenizer_extractor([(question, context)], padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            model_output = self.boolean_model_extractor(**encoded_input)
            probabilities = torch.softmax(model_output.logits, dim=-1).cpu().tolist()

        probability_no = [round(prob[0], 2) for prob in probabilities]
        probability_yes = [round(prob[1], 2) for prob in probabilities]

        return probability_yes, probability_no

    def extract_answer(self, question_type, entities, question, context):
        """
        Handles extraction of answers based on question type.

        Args:
            question_type: 'Boolean' or 'Entity'
            entities: list of the linked entities
            question: user question provided
            context: LLM's response

        Returns:
            in case question type is boolean, returns 'Yes' or 'No'
            if question is entity, return the extracted entity from model's answer extraction
        """
        if question_type == "Boolean":
            pyes, pno = self.boolean_answer_extraction(question, context)
            if pyes > pno:
                A = "Yes"
            else:
                A = "No"
            return A
        else:
            ext_ent = self.entity_answer_extraction(question, context)
            A = utils.extract_entity(ext_ent, entities)
            return A
