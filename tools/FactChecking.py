from SPARQLWrapper import SPARQLWrapper, JSON
import tensorflow_hub as hub
import numpy as np
import os
import logging
import re

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
logging.getLogger("tensorflow").setLevel(logging.ERROR)


def query_entity_properties(entity_id):
    """
    Queries and returns the properties of a Wikidata entity.

    Parameters:
    - entity_id (str): Wikidata entity ID (e.g., "Q1").

    Returns:
    - dict: A dictionary of properties and their values for the given entity.
    """

    sparql = SPARQLWrapper(
        "https://query.wikidata.org/sparql", agent="OlafJanssen from PAWS"
    )
    query = f"""
    SELECT ?propertyLabel ?value ?valueLabel WHERE {{
      wd:{entity_id} ?p ?statement .
      ?property wikibase:claim ?p.
      ?property wikibase:statementProperty ?ps.
      ?statement ?ps ?value .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    properties = {}
    for result in results["results"]["bindings"]:
        prop = result["propertyLabel"]["value"]
        value = result["value"]["value"]

        if value.startswith("http://www.wikidata.org/entity/"):
            value_id = value.split("/")[-1]
        else:
            value_id = value

        if prop in properties:
            properties[prop].append(value_id)
        else:
            properties[prop] = [value_id]

    return properties


def get_most_similar_property(query, properties):
    """
    Finds the most similar property to the given query using sentence embeddings.

    Parameters:
    - query (str): The query string to compare against.
    - properties (dict): A dictionary of properties.

    Returns:
    - tuple: A tuple containing the most similar property and its values.
    """

    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    query_embedding = embed([query])[0]
    property_embeddings = embed(list(properties.keys()))

    similarity = np.inner(query_embedding, property_embeddings)

    most_similar_index = np.argmax(similarity)
    most_similar_property = list(properties.keys())[most_similar_index]

    return most_similar_property, properties[most_similar_property]


def is_entity(value):
    """
    Checks if a given value is a Wikidata entity ID.

    Parameters:
    - value (str): The value to check.

    Returns:
    - bool: True if the value matches the Wikidata entity ID pattern, False otherwise.
    """
    return bool(re.match(r"Q\d+", value))


def get_entity_label(entity_id):
    """
    Retrieves the label of a Wikidata entity in English.

    Parameters:
    - entity_id (str): The Wikidata entity ID.

    Returns:
    - str or None: The label of the entity, or None if not found.
    """

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = f"""
    SELECT ?label WHERE {{
        wd:{entity_id} rdfs:label ?label .
        FILTER(LANG(?label) = "en")
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]["label"]["value"]
    else:
        return None


def check_relationship(entity_id, relationship, subject_id):
    """
    Checks if a specified relationship exists between two entities.

    Parameters:
    - entity_id (str): The Wikidata entity ID.
    - relationship (str): The relationship to check.
    - subject_id (str): The subject entity ID or name.

    Returns:
    - bool: True if the relationship exists, False otherwise.
    """

    properties = query_entity_properties(entity_id)
    most_similar_property, values = get_most_similar_property(relationship, properties)

    subject_is_entity = is_entity(subject_id)

    for value in values:
        if subject_is_entity:
            if subject_id == value:
                return True
        else:
            if is_entity(value):
                entity_label = get_entity_label(value)
                if entity_label and subject_id.lower() in entity_label.lower():
                    return True
            else:
                if subject_id.lower() in value.lower():
                    return True

    return False

def fact_check_triple(question_type, answer, triple):
    fact_check_res = check_relationship(
        triple["subject"], triple["relation"], triple["object"]
    )
    print("==========================")
    print("Fact check result:")
    print(fact_check_res)
    print("correct/incorrect:")
    if question_type == "Boolean":
        if (answer == 'Yes' and fact_check_res == True) or (
                answer == 'No' and fact_check_res == False
        ):
            print("CORRECT")
            return "correct"
        else:
            print("INCORRECT")
            return "incorrect"

    if question_type == "Entity" or question_type == "Completion":
        if fact_check_res == True:
            print("CORRECT")
            return "correct"

        else:
            print("INCORRECT")
            return "incorrect"
