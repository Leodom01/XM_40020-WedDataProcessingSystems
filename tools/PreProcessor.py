from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from stanza.server import CoreNLPClient
import spacy
from nltk import ne_chunk, pos_tag
class PreProcessor:
    def __init__(self, text_to_preprocess=""):
        self.text_to_preprocess = text_to_preprocess
        self.tokenized_text = word_tokenize(self.text_to_preprocess)

    def pos(self):
        print(self.tokenized_text)
        return pos_tag(self.tokenized_text)
    def replace_text(self, text):
        self.text_to_preprocess = text
        self.tokenized_text = ""
        self.tokenize()

    def tokenize(self):
        if len(self.tokenized_text) == 0:
            # Classic tokenizer
            self.tokenized_text = word_tokenize(self.text_to_preprocess)

        return self.tokenized_text

    def np_chunking(self):
        # Named entities aware chunker
        tokens = word_tokenize(self.text_to_preprocess)
        chunks = ne_chunk(pos_tag(tokens))
        print("Chunked list:")
        print([w[0] if isinstance(w, tuple) else " ".join(t[0] for t in w) for w in chunks])

    def lemmatize(self):
        if not self.tokenized_text:
            self.tokenize()
        lemmatizer = WordNetLemmatizer()
        lemmatized_text = [lemmatizer.lemmatize(word) for word in self.tokenized_text]
        return lemmatized_text

    def stem(self):
        if not self.tokenized_text:
            self.tokenize()
        stemmer = PorterStemmer()
        stemmed_text = [stemmer.stem(word) for word in self.tokenized_text]
        return stemmed_text

    def pipeline(self):
        # We think stemming could work worse
        return self.lemmatize()

    def coref(self, text):
        nlp = spacy.load("en_coreference_web_trf")
        doc = nlp(text)
        offset = 0
        reindex = []
        for chain in doc.spans:
            for idx, span in enumerate(doc.spans[chain]):
                if idx > 0:
                    reindex.append([span.start_char, span.end_char, doc.spans[chain][0].text])

        for span in sorted(reindex, key=lambda x: x[0]):
            text = text[0:span[0] + offset] + span[2] + text[span[1] + offset:]
            offset += len(span[2]) - (span[1] - span[0])

        return text


if __name__ == "__main__":
    pass