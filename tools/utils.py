import re
"""
This module provide utility functions that are used throughout the system.
"""

def is_wikidata_entity(text):
    """
    Checks if the given text matches the pattern of a Wikidata entity (QID).

    Parameters:
    text (str): The text to be checked.

    Returns:
    bool: True if the text matches the Wikidata entity pattern (QID), False otherwise.
    """
    pattern = r'^Q\d+$'
    return bool(re.match(pattern, text))

def statement_with_wikidatIDs(fact_statement, ent_list):
    """
    Replaces entity mentions in the factual statement with their corresponding Wikidata IDs.

    Parameters:
    fact_statement (str): The fact statement containing names.
    ent_list (list): List of dictionaries containing 'name' and 'link' keys.

    Returns:
    str: The modified fact statement with Wikidata IDs.

    Note:
    If no replacements are made, the original fact_statement is returned.
    """
    input_string = fact_statement
    for ent in ent_list:
        name = ent['name']
        wikidata_ID = ent['wikidata_ID']
        # extract the Wikidata ID and assign it
        input_string = input_string.replace(str(name), wikidata_ID)
    if input_string == None:
        return fact_statement
    else:
        return input_string

def find_suitable_triple(triples):
    """
    Finds the best triple from a list of triples where both subject and object are Wikidata entities.
    The chosen triple should have the biggest predicate sequence. For example, in the sentence
    "Rome is the capital of Italy", relation extraction returns the triples containing <Rome, is, Italy>,
    <Rome, is the capital of, Italy>. Thus, by using the largest predicate we were able to achieve better results.

    Parameters:
    triples (list): List of dictionaries containing 'subject', 'relation', and 'object' keys.

    Returns:
    dict or None: The best triple satisfying the conditions or None if no such triple is found.
    """
    trpl = None
    max_len = 0
    for triple in triples:
        # subject and object should be linked entities
        if is_wikidata_entity(triple['subject']) and is_wikidata_entity(triple['object']):
            # finding the largest predicate
            if len(triple['relation']) >= max_len:
                trpl = triple
    return trpl


def extract_text(input_text):
    """
    Extracts the text between "Question: " and " Answer:" from the given input text.

    Args:
    input_text (str): The input string containing the pattern "Question: X Answer:"

    Returns:
    str or None: The extracted text if the pattern is found, else None.
    """
    pattern = r"Question: (.*?) Answer:"
    match = re.search(pattern, input_text)

    if match:
        return match.group(1)
    else:
        return input_text

def extract_entity(ans, entities):
    for ent in entities:
        if str(ent['name']).lower() == ans.lower():
            return ent

def load_data(input_path):
    data = {}
    with open(input_path) as openfileobject:
        for line in openfileobject:
            prts = line.rstrip().split('\t')
            data[prts[0]] = {
                'Q': prts[1]
            }
        openfileobject.close()
    return data

def output(data, out_path):
    with open(out_path, 'w') as fw:
        for qID in data.keys():
            fw.write(f"{qID}\tR\"{data[qID]['R']}\n")
            fw.write(f"{qID}\tA\"{data[qID]['A']}\n")
            fw.write(f"{qID}\tC\"{data[qID]['C']}\n")
            for ent in data[qID]['E']:
                fw.write(f"{qID}\tE\"{ent['name']}\t{ent['link']}\n")

