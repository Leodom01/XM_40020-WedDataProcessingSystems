from CandidateRanking import *

# Just a playground

context1 = "Queen Elizabeth II died last year"
context2 = "I like Queen's second studio album"
named_entity = "Queen"

most_relevant_entity = link_entity(context1, named_entity)
print(f"Relevant Entity on Wikidata for {context1}:")
print(f"Item: {most_relevant_entity['Item']}")
print(f"Label: {most_relevant_entity['Label']}")
print(f"Description: {most_relevant_entity['Description']}")
print(f"+----------------------------+")

most_relevant_entity = link_entity(context2, named_entity)
print(f"Relevant Entity on Wikidata for {context2}:")
print(f"Item: {most_relevant_entity['Item']}")
print(f"Label: {most_relevant_entity['Label']}")
print(f"Description: {most_relevant_entity['Description']}")
