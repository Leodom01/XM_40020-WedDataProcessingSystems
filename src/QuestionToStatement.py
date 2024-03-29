import nltk
import spacy
from nltk import word_tokenize, pos_tag
import src.utils as utils
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
"""
Handles creating factual statement. It mainly handles Wh questions. This is because the open relation extraction 
method chosen can handle boolean structure but struggles with Wh question/answers.
"""
def find_wh_word(question):
    # Tokenize the question and perform part-of-speech tagging
    tokens = word_tokenize(question)
    tagged_tokens = pos_tag(tokens)

    # Perform constituency parsing
    grammar = r"""
        NP: {<DT>?<JJ>*<NN>} # Chunk Noun Phrases
        WH: {<WRB|WP|WDT>}   # Chunk WH-words
        VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk Verb Phrases
        CLAUSE: {<NP><VP>}   # Chunk Clauses
        """
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(tagged_tokens)

    # Traverse the parsed tree to find the WH-word
    for subtree in result.subtrees():
        if subtree.label() == 'WH':
            wh_word = " ".join(word for word, tag in subtree.leaves())
            return wh_word

    return None


def replace_wh_word_with_entity(question, entity):
    # Find the WH-word in the question
    wh_word = find_wh_word(question)

    if wh_word:
        # Replace the WH-word with the provided entity
        replaced_question = question.replace(wh_word, str(entity))
        return replaced_question
    else:
        return str(entity)+question


def construct_factual_statement(question_type, entities, question, answer):
    fact_statement = ''
    # not changing the structure of boolean questions since stanford openie is able to extract triples from it
    if question_type == "Boolean":
        return utils.statement_with_wikidatIDs(question, entities)
    else:
        if question_type == "Entity":
            tmp = replace_wh_word_with_entity(question, answer['wikidata_ID'])
            return utils.statement_with_wikidatIDs(tmp, entities)
        if question_type == "Completion":
            tmp = question + " " + answer['wikidata_ID']
            return utils.statement_with_wikidatIDs(tmp, entities)



if __name__ == "__main__":
    replace_wh_word_with_entity("What is the capital of Italy?", "Rome")