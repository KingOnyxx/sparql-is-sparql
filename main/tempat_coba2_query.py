from SPARQLWrapper import SPARQLWrapper, JSON

# GraphDB SPARQL endpoint
sparql = SPARQLWrapper("http://DESKTOP-V5G8723:7200/repositories/airports")

# Set the SPARQL query
sparql.setQuery("""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX v: <http://myairports.com/vocab#>
PREFIX : <http://myairports.com/data/>

select distinct ?navaid ?navaid_label ?navaid_ident where {
    ?navaid v:icao_code "CYCD";
    		rdfs:label ?navaid_label;
    		v:ident ?navaid_ident .
    ?airport v:ident "CYCD" .
    
   
}  order by ?navaid_label
""")

# Set the output format to JSON
sparql.setReturnFormat(JSON)

# Execute the query
results = sparql.query().convert()



if (len(results["results"]["bindings"]) == 0):
    raise ValueError


navaids = []
navaid_labels = []
navaid_idents = []

for result in results["results"]["bindings"]:
    navaids.append(result["navaid"]["value"])
    navaid_labels.append(result["navaid_label"]["value"])
    navaid_idents.append(result["navaid_ident"]["value"])

print(navaids)
print(navaid_labels)
print(navaid_idents)




