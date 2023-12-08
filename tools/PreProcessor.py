from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from stanza.server import CoreNLPClient
import spacy
from nltk import ne_chunk, pos_tag
class PreProcessor:
    def __init__(self, text_to_preprocess=""):
        self.text_to_preprocess = text_to_preprocess
        self.tokenized_text = word_tokenize(self.text_to_preprocess)

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