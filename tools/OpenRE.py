from openie import StanfordOpenIE
import itertools
import sys
sys.path.append("..")
import opennre
'''
This module is for open relation extraction on raw text using the Stanford Open IE
https://nlp.stanford.edu/software/openie.html
Python wrapper https://github.com/philipperemy/stanford-openie-python
'''
class OpenRE:
    def __init__(self, text):
        self.text = text

    def extract_relations_stanford(self):
        # https://stanfordnlp.github.io/CoreNLP/openie.html#api
        # Default value of openie.affinity_probability_cap was 1/3.
        properties = {
            'openie.affinity_probability_cap': 1 / 3,
        }
        with StanfordOpenIE(properties=properties) as client:
            annotated_text = client.annotate(self.text)
            for triple in annotated_text:
                print('|-', triple)
            # to generate an image of the relations extracted, must install graphviz,
            # graph_image = 'graph.png'
            # client.generate_graphviz_graph(self.text, graph_image)
            # print('Graph generated: %s.' % graph_image)

    def extract_relations_openNRE(self, annotated_doc, threshhold):
        triples = []
        model = opennre.get_model('wiki80_cnn_softmax')
        for sent in annotated_doc.sents:
            for permutation in itertools.permutations(set(sent.ents), 2):
                source = permutation[0]
                target = permutation[1]
                input = {
                    'text': sent.text,
                    'h': {'pos': (source.start_char - sent.start_char, source.end_char - sent.start_char)},
                    't': {'pos': (target.start_char - sent.start_char, target.end_char - sent.start_char)}}
                res = model.infer(input)
                if res[1] >= threshhold:
                    triples.append((source.text, target.text, res[0]))
        return triples

if __name__ == "__main__":
    text = 'Obama was born in Hawaii. Elon, The American investor, founded tesla'
    OIE = OpenRE(text)
    OIE.extract_relations_stanford()

