from SPARQLWrapper import SPARQLWrapper, JSON

# GraphDB SPARQL endpoint
sparql = SPARQLWrapper("http://DESKTOP-V5G8723:7200/repositories/airports")

# Set the SPARQL query
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX : <http://myairports.com/data/>            
    
    select ?iso_country ?label where {
        ?iso_country rdf:type :country ;
                rdfs:label ?label .
            
        FILTER(?iso_country = :BN)
    } limit 100
""")

# Set the output format to JSON
sparql.setReturnFormat(JSON)

# Execute the query
results = sparql.query().convert()



if (len(results["results"]["bindings"]) == 0):
    raise ValueError


countries = []


for result in results["results"]["bindings"]:
    print(result)
    countries.append(result["label"]["value"])


print(countries)




