import re

"""
This module provide utility functions that are used throughout the system.
"""

def is_wikidata_entity(text):
    pattern = r'^Q\d+$'
    return bool(re.match(pattern, text))

def statement_with_wikidatIDs(fact_statement, ent_list):
    input_string = fact_statement
    for word_dict in ent_list:
        name = word_dict['name']
        link = word_dict['link']
        input_string = input_string.replace(str(name), link.split('/')[-1])
    if input_string == None:
        return fact_statement
    else:
        return input_string

def find_best_triple(triples):
    trpl = None
    max_len = 0
    for triple in triples:
        if is_wikidata_entity(triple['subject']) and is_wikidata_entity(triple['object']):
            if len(triple['relation']) >= max_len:
                trpl = triple

    return trpl