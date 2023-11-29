from SPARQLWrapper import SPARQLWrapper, JSON


def query_wikidata(search_term):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

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


if __name__ == "__main__":
    dummy_search_term = "obama"
    search_results = query_wikidata(dummy_search_term)

    for result in search_results:
        print(f"Item: {result['Item']}")
        print(f"Label: {result['Label']}")
        print(f"Description: {result['Description']}")
        print(f"Sitelink Count: {result['Sitelink Count']}")
        print("------------------------------------------------")
