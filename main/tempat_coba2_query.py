from SPARQLWrapper import SPARQLWrapper, JSON

# GraphDB SPARQL endpoint
# punya joel
sparql = SPARQLWrapper("http://DESKTOP-V5G8723:7200/repositories/airports")

# punya adrial
# sparql = SPARQLWrapper("http://DESKTOP-CMK0990:7200/repositories/airport")
final_result=dict()
# Set the SPARQL query
id = "Dubai_Emirate"
# print(type(id))
sparql.setQuery("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX v: <http://myairports.com/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://myairports.com/data/>
                
SELECT ?region ?label ?hasID ?hasLocalCode ?partOf
WHERE {
    ?region rdf:type :region .
    OPTIONAL { ?region rdfs:label ?label . }
    OPTIONAL { ?region v:hasID ?hasID . }
    OPTIONAL { ?region v:hasLocalCode ?hasLocalCode . }
    OPTIONAL { ?region v:partOf ?partOf . }
    FILTER(?label = \"""" + id + """\")
}
LIMIT 100
""")


# Set the output format to JSON
sparql.setReturnFormat(JSON)

# Execute the query
results = sparql.query().convert()

# print(type(results))


if (len(results["results"]["bindings"]) == 0):
    raise ValueError

result = results["results"]["bindings"][0]

for key in result.keys():
    final_result[key] = result[key]["value"]

# print(final_result)





