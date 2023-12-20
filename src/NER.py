import spacy
from spacy import displacy
"""
This module handles Named Entity Recognition.
"""
class NER:
    def __init__(self):
        self.model = spacy.load("en_core_web_sm")
    def ner_spacy(self, text):
        """
        Loads the spaCy model for Named Entity Recognition (NER).

        Returns:
        spacy.tokens.doc.Doc: The processed Doc object with named entities.

        Raises:
        OSError: If the spaCy model loading fails.
        """
        return self.model(text)


    def spacyVisulizer(self, doc):
        """
        Visualizes the named entities in the provided spaCy Doc object and serves it on an available port.

        Parameters:
        doc (spacy.tokens.doc.Doc): The spaCy Doc object containing named entities.
        """
        displacy.serve(doc, style="ent", auto_select_port=True)







