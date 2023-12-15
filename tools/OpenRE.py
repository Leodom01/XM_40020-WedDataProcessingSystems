from stanza.server import CoreNLPClient
import os
import re
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

    def is_wikidata_entity(self, text):
        pattern = r'^Q\d+$'
        return bool(re.match(pattern, text))

    def statement_with_wikidatIDs(self, fact_statement, ent_list):
        input_string = fact_statement
        for word_dict in ent_list:
            name = word_dict['name']
            link = word_dict['link']
            input_string = input_string.replace(str(name), link.split('/')[-1])
        if input_string == None:
            return fact_statement
        else:
            return input_string

    def find_best_triple(self, triples):
        trpl = ''
        max_len = 0
        for triple in triples:
            if self.is_wikidata_entity(triple['subject']) and self.is_wikidata_entity(triple['object']):
                if len(triple['relation']) >= max_len:
                    trpl = triple

        return trpl

