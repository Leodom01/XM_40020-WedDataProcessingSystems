from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

search_term = "Apple"

query = (
    """
SELECT ?item ?itemLabel ?itemDescription (COUNT(?sitelink) AS ?linkCount) WHERE {
  SERVICE wikibase:mwapi {
      bd:serviceParam wikibase:api "EntitySearch".
      bd:serviceParam wikibase:endpoint "www.wikidata.org".
      bd:serviceParam mwapi:search "%s".
      bd:serviceParam mwapi:language "en".
      ?item wikibase:apiOutputItem mwapi:item.
  }
  OPTIONAL { ?item rdfs:label ?itemLabel. FILTER(LANG(?itemLabel) = "en") }
  OPTIONAL { ?item schema:description ?itemDescription. FILTER(LANG(?itemDescription) = "en") }
  OPTIONAL { ?item wikibase:sitelinks ?sitelink. }
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

for result in results["results"]["bindings"]:
    print(f"Item: {result['item']['value']}")
    print(f"Label: {result.get('itemLabel', {}).get('value', 'No label')}")
    print(
        f"Description: {result.get('itemDescription', {}).get('value', 'No description')}"
    )
    print("------------------------------------------------")
