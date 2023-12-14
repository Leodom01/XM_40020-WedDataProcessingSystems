from SPARQLWrapper import SPARQLWrapper, JSON
import tensorflow_hub as hub
import numpy as np
import os
import logging
import re

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
logging.getLogger("tensorflow").setLevel(logging.ERROR)


def query_entity_properties(entity_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

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
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    query_embedding = embed([query])[0]
    property_embeddings = embed(list(properties.keys()))

    similarity = np.inner(query_embedding, property_embeddings)

    most_similar_index = np.argmax(similarity)
    most_similar_property = list(properties.keys())[most_similar_index]

    return most_similar_property, properties[most_similar_property]


def is_entity(value):
    return bool(re.match(r"Q\d+", value))


def get_entity_label(entity_id):
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


# print("Is Managua the capital of Nicaragua?", end=": ")
# print(check_relationship("Q811", "capital", "Q3274"))

# print("Is Biden the current president of US?", end=": ")
# print(check_relationship("Q30", "current president", "Q6279"))

# print("Is Obama the current president of US?", end=": ")
# print(check_relationship("Q30", "current president", "Q76"))

# print("Is Jupiter the largest planet in solar system?", end=": ")
# print(check_relationship("Q544", "largest planet", "Q319"))

# print("Is da Vinci the painter of Mona Lisa?", end=": ")
# print(check_relationship("Q12418", "painter", "Q762"))

# print("Is Tokyo the capital of Japan?", end=": ")
# print(check_relationship("Q17", "capital", "Q1490"))

# print("Did Shakespear write the Romeo and Julliet?", end=": ")
# print(check_relationship("Q83186", "writer", "Q692"))

# print("Is declaration of independence signed in 1776", end=": ")
# print(check_relationship("Q127912", "date signed", "1776"))

print("Did Shakespear write the Romeo and Julliet?", end=": ")
print(check_relationship("Q83186", "writer", "Shakespear"))

# properties = query_entity_properties("Q127912")

# for prop, values in properties.items():
#     print(f"{prop}:\n\t{', '.join(values)}\n{'-'*40}")
