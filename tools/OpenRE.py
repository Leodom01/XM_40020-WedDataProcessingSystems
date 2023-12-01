from openie import StanfordOpenIE

'''
This module is for open relation extraction on raw text using the Stanford Open IE
https://nlp.stanford.edu/software/openie.html
Python wrapper https://github.com/philipperemy/stanford-openie-python
'''
class OpenRE:
    def __init__(self, text):
        self.text = text

    def extract_relations(self):
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

if __name__ == "__main__":
    text = 'Barack Obama was born in Hawaii. Richard Manning wrote this sentence.'
    OIE = OpenRE(text)
    OIE.extract_relations()
