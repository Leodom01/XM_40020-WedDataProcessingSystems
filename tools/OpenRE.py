from stanza.server import CoreNLPClient
import re
'''
This module handles open relation extraction on text using the Stanford Open IE
ttps://nlp.stanford.edu/software/openie.html
Python wrapper stanza project https://github.com/stanfordnlp/stanza
'''

class OpenRE:
    def __init__(self):
        """
        Initializes the CoreNLPClient with the openie pipeline.

        This method sets up the CoreNLPClient instance for extracting relations using OpenIE.
        """
        self.client = CoreNLPClient(
            annotators=['openie'],
            timeout=30000,
            memory='6G',
            be_quiet=True)

    def extract_relations_stanford(self, text):
        """
        Extracts relations using Stanford CoreNLP's OpenIE from the provided text.

        Parameters:
        text (str): The input text for relation extraction.

        Returns:
        list: A list of dictionaries containing extracted triples (subject, relation, object).
        """
        document = self.client.annotate(text, output_format='json')
        triples = []
        for sentence in document['sentences']:
            for triple in sentence['openie']:
                triples.append({
                    'subject': triple['subject'],
                    'relation': triple['relation'],
                    'object': triple['object']
                })
        return triples