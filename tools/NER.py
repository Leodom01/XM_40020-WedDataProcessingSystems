import spacy
from spacy import displacy
"""
This module handles Named Entity Recognition.
"""
class NER:
    def __init__(self, raw_text, tokens=''):
        self.tokens = tokens
        self.raw_text = raw_text

    def ner_spacy(self):
        """
        Loads the spaCy model for Named Entity Recognition (NER).

        Returns:
        spacy.tokens.doc.Doc: The processed Doc object with named entities.

        Raises:
        OSError: If the spaCy model loading fails.
        """
        spacyNER = spacy.load("en_core_web_sm")
        return spacyNER(self.raw_text)


    def spacyVisulizer(self, doc):
        """
        Visualizes the named entities in the provided spaCy Doc object and serves it on an available port.

        Parameters:
        doc (spacy.tokens.doc.Doc): The spaCy Doc object containing named entities.
        """
        displacy.serve(doc, style="ent", auto_select_port=True)




