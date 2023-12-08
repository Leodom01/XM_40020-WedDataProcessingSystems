import stanza
from stanza.server import CoreNLPClient
import PreProcessor
import time
'''
This module is for open relation extraction on raw text using the Stanford Open IE
https://nlp.stanford.edu/software/openie.html
Python wrapper https://github.com/philipperemy/stanford-openie-python
'''
class OpenRE:
    def __init__(self):
        stanza.install_corenlp()

    def extract_relations_stanford(self, text):
        client = CoreNLPClient(timeout=150000000, be_quiet=True, annotators=['openie'],
                               endpoint='http://localhost:9001')
        client.start()
        document = client.annotate(text, output_format='json')
        triples = []
        for sentence in document['sentences']:
            for triple in sentence['openie']:
                triples.append({
                    'subject': triple['subject'],
                    'relation': triple['relation'],
                    'object': triple['object']
                })
        return triples

if __name__ == "__main__":
    pp = PreProcessor.PreProcessor()
    text = 'Obama was born in Hawaii. Elon founded tesla. He also founded SpaceX'
    text = pp.coref(text)
    OIE = OpenRE()
    triples = OIE.extract_relations_stanford(text)
    for triple in triples:
        print(triple)

