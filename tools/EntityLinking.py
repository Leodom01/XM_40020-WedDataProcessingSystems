from CandidateRanking import *

# Just a playground

context = "i like queen's second studio album"
named_entity = "queen"
most_relevant_entity = link_entity(context, named_entity)

print("Relevant Entity on Wikidata:")
print(f"Item: {most_relevant_entity['Item']}")
print(f"Label: {most_relevant_entity['Label']}")
print(f"Description: {most_relevant_entity['Description']}")
