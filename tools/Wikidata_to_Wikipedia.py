from SPARQLWrapper import SPARQLWrapper, JSON


def wikidata_to_wikipedia(wikidata_id, language="en"):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    query = """
    SELECT ?article WHERE {
      BIND(wd:%s AS ?item)
      ?article schema:about ?item.
      ?article schema:inLanguage "%s".
      ?article schema:isPartOf <https://%s.wikipedia.org/>.
    }
    """ % (
        wikidata_id,
        language,
        language,
    )

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]["article"]["value"]
    else:
        return "No Wikipedia article found for this Wikidata ID"


wikidata_id = "Q12418"
wikipedia_url = wikidata_to_wikipedia(wikidata_id)
print(wikipedia_url)
