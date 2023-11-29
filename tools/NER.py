import spacy
from spacy import displacy

class NER:
    def __init__(self, raw_text, tokens=''):
        self.tokens = tokens
        self.raw_text = raw_text
    '''
    Loads the spacy model for NER
    '''
    def ner_spacy(self):
        try:
            spacyNER = spacy.load("en_core_web_sm")
        except:
            print("Download the spacy model with the following command:")
            print("$ python -m spacy download en")
            return
        return spacyNER(self.raw_text)

    '''
    Visualizes the named entities at an available port. 
    '''
    def spacyVisulizer(self, doc):
        displacy.serve(doc, style="ent", auto_select_port=True)




