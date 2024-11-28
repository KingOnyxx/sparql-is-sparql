from SPARQLWrapper import SPARQLWrapper, JSON

# GraphDB SPARQL endpoint
sparql = SPARQLWrapper("http://DESKTOP-V5G8723:7200/repositories/airports")

# Set the SPARQL query
sparql.setQuery("""
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object
    }
    LIMIT 10
""")

# Set the output format to JSON
sparql.setReturnFormat(JSON)

# Execute the query
results = sparql.query().convert()

print(type(results))

# Handle the results (e.g., print them)
for result in results["results"]["bindings"]:
    print(result)