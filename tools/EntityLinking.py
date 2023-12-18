from SPARQLWrapper import SPARQLWrapper, JSON
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class EntityLinker:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    def query_wikidata(self, search_term):
        """
        Queries Wikidata for entities matching the given search term.

        Parameters:
        - search_term (str): The term to search for in Wikidata.

        Returns:
        - list: A list of formatted results containing Wikidata entity information.
        """

        sparql = SPARQLWrapper(
            "https://query.wikidata.org/sparql", agent="Aynaz from UvA"
        )

        query = (
            """
            SELECT ?item ?itemLabel ?itemDescription (COUNT(DISTINCT ?sitelink) AS ?linkCount) WHERE {
            SERVICE wikibase:mwapi {
                bd:serviceParam wikibase:api "EntitySearch".
                bd:serviceParam wikibase:endpoint "www.wikidata.org".
                bd:serviceParam mwapi:search "%s".
                bd:serviceParam mwapi:language "en".
                ?item wikibase:apiOutputItem mwapi:item.
            }
            OPTIONAL { ?item rdfs:label ?itemLabel. FILTER(LANG(?itemLabel) = "en") }
            OPTIONAL { ?item schema:description ?itemDescription. FILTER(LANG(?itemDescription) = "en") }
            OPTIONAL { ?sitelink schema:about ?item. ?sitelink schema:isPartOf [ wikibase:wikiGroup "wikipedia" ] }
            FILTER NOT EXISTS { ?item wdt:P31/wdt:P279* wd:Q4167410 }
            }
            GROUP BY ?item ?itemLabel ?itemDescription
            ORDER BY DESC(?linkCount)
            LIMIT 10
            """
            % search_term
        )

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        results = sparql.query().convert()

        formatted_results = []
        for result in results["results"]["bindings"]:
            linkCount = int(result["linkCount"]["value"])
            if linkCount > 3:
                formatted_results.append(
                    {
                        "Item": result["item"]["value"],
                        "Label": result.get("itemLabel", {}).get("value", "No label"),
                        "Description": result.get("itemDescription", {}).get(
                            "value", "No description"
                        ),
                        "Sitelink Count": result["linkCount"]["value"],
                    }
                )

        return formatted_results

    def link_entity(self, context, named_entity):
        """
        Finds the most relevant Wikidata entity for a given named entity and context.

        Parameters:
        - context (str): The context in which the named entity is mentioned.
        - named_entity (str): The named entity to be linked.

        Returns:
        - dict: The most relevant Wikidata entity, or None if no match is found.
        """

        candidates = self.query_wikidata(named_entity)

        if not candidates:
            print(f"No matching candidates found for entity {named_entity}.")
            return

        model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

        context = f"title: {named_entity}, description: {context}"
        context_embedding = model.encode(context)

        candidate_texts = [
            f'title: {candidate["Label"]}, description: {candidate["Description"]}'
            for candidate in candidates
        ]

        candidate_embeddings = model.encode(candidate_texts)

        similarities = cosine_similarity([context_embedding], candidate_embeddings)[0]

        most_relevant_index = np.argmax(similarities)

        return candidates[most_relevant_index]['Item']


if __name__ == "__main__":
    linker = EntityLinker()
    context = "Does lebron james play in the lakers"
    named_entity = "lebron james"
    print(linker.link_entity(context, named_entity))
