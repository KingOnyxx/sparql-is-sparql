from SPARQLWrapper import SPARQLWrapper, JSON

# GraphDB SPARQL endpoint
# punya joel
# sparql = SPARQLWrapper("http://DESKTOP-V5G8723:7200/repositories/airports")

# punya adrial
# sparql = SPARQLWrapper("http://DESKTOP-CMK0990:7200/repositories/airport")
sparql = SPARQLWrapper("http://34.50.87.161:7200/repositories/airports")
final_result=dict()
# Set the SPARQL query
# id = "Dubai_Emirate"
# print(type(id))
sparql.setQuery("""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://myairports.com/data/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX v: <http://myairports.com/data/>

    SELECT * WHERE {{
        {
            ?airport rdf:type :airport;
                    rdfs:label ?airport_label .
            FILTER(CONTAINS(LCASE(?airport_label), "''' + id + '''"))
        }
        UNION
        { 
            ?region rdf:type :region;
                    rdfs:label ?region_label .
            BIND(
                IF(
                    CONTAINS(LCASE(?region_label), "unassigned"),
            		SUBSTR(STR(?region), 28),
                    ?region_label
                ) AS ?region_label_result
            )
            FILTER(CONTAINS(LCASE(?region_label_result), "''' + id + '''"))

    }
        UNION
        {
            ?navaid rdf:type :navaid;
                    rdfs:label ?navaid_label .
            FILTER(CONTAINS(LCASE(?navaid_label), "''' + id + '''"))
        }
        UNION
        {
            ?runway rdf:type :Runway;
                    rdfs:label ?runway_label .
            FILTER(CONTAINS(LCASE(?runway_label), "''' + id + '''"))
        }
        UNION
        {
            ?country rdf:type v:country;
                    rdfs:label ?country_label .
            ?code v:isoHasLabel ?label2 .
            FILTER(?country = ?code) .
            FILTER(CONTAINS(LCASE(?country_label), "''' + id + '''"))
        }
    }}
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

print(final_result)





