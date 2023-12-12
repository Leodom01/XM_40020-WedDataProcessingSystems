from stanza.server import CoreNLPClient
import os

corenlp_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '../stanza_corenlp'))
os.environ['CORENLP_HOME'] = corenlp_home
# import PreProcessor
'''
This module is for open relation extraction on raw text using the Stanford Open IE
https://nlp.stanford.edu/software/openie.html
Python wrapper https://github.com/philipperemy/stanford-openie-python
'''
class OpenRE:
    def __init__(self):
        # stanza.install_corenlp()
        pass

    def extract_relations_stanford(self, text):
        with CoreNLPClient(
                annotators=['openie'],
                timeout=30000,
                memory='6G',
                be_quiet = True) as client:
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

