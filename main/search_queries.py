from SPARQLWrapper import SPARQLWrapper, JSON

def search_queries(id, sparql):
    print(type(id))
    print(id)
    final_result = dict()

    # Set the SPARQL query
    sparql.setQuery('''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://myairports.com/data/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT * WHERE {
    ?airport rdf:type :airport;
    rdfs:label ?airport_label .
    FILTER(CONTAINS(LCASE(?airport_label), "''' + id + '''"))
}

    ''')

    # Set the output format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query
    results = sparql.query().convert()

    print(type(results))


    if (len(results["results"]["bindings"]) == 0):
        raise ValueError


    airports = []
    airport_labels = []

    for result in results["results"]["bindings"]:
        airports.append(result["airport"]["value"])
        airport_labels.append(result["airport_label"]["value"])
    
    final_result["airports"] = airports
    final_result["airport_labels"] = airport_labels

    return final_result