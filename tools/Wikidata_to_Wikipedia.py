def wikidata_to_wikipedia(wikidata_id):
    """
    Fetches the Wikipedia URL for a given Wikidata ID.

    Parameters:
    - wikidata_id (str): Wikidata entity ID.

    Returns:
    - str: Wikipedia article URL in English or a not-found message.
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    language = "en"

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
