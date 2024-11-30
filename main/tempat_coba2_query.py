from SPARQLWrapper import SPARQLWrapper, JSON

# GraphDB SPARQL endpoint
# punya joel
# sparql = SPARQLWrapper("http://DESKTOP-V5G8723:7200/repositories/airports")

# punya adrial
sparql = SPARQLWrapper("http://DESKTOP-CMK0990:7200/repositories/airport")
final_result=dict()
# Set the SPARQL query
sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX c: <http://example.org/countries/>
    PREFIX v: <http://myairports.com/data/>

    SELECT DISTINCT * WHERE {{
        ?country v:isPartOfRegion ?type .

        OPTIONAL {{?country v:hasPopulation ?Population . }}
        OPTIONAL {{?country v:hasAreaInSquareMiles ?AreaInSquareMiles . }}
        OPTIONAL {{?country v:hasPopulationDensityPerSquareMiles ?PopulationDensityPerSquareMiles . }}
        OPTIONAL {{?country v:hasCoastlineRatio ?CoastlineRatio . }}
        OPTIONAL {{?country v:hasNetMigration ?NetMigration . }}
        OPTIONAL {{?country v:hasInfantMortality ?InfantMortality . }}
        OPTIONAL {{?country v:hasGDPInUSD ?GDPInUSD . }}
        OPTIONAL {{?country v:hasLiteracyRate ?hasLiteracyRate . }}
        OPTIONAL {{?country v:hasPhones ?hasPhones . }}
        OPTIONAL {{?country v:arablePercentage ?arablePercentage . }}
        OPTIONAL {{?country v:cropsPercentage ?cropsPercentage . }}
        OPTIONAL {{?country v:othersPercentage ?othersPercentage . }}
        OPTIONAL {{?country v:hasClimate ?hasClimate . }}
        OPTIONAL {{?country v:hasBirthrate ?hasBirthrate . }}
        OPTIONAL {{?country v:hasDeathrate ?hasDeathrate . }}
        OPTIONAL {{?country v:hasAgricultureRatio ?hasAgricultureRatio . }}
        OPTIONAL {{?country v:hasIndustryRatio ?hasIndustryRatio . }}
        OPTIONAL {{?country v:hasServiceRatio ?hasServiceRatio . }}
        OPTIONAL {{?country v:label ?label . }}

        FILTER(?country = c:Afghanistan).
                }}

""")

# Set the output format to JSON
sparql.setReturnFormat(JSON)

# Execute the query
results = sparql.query().convert()

print(type(results))


if (len(results["results"]["bindings"]) == 0):
    raise ValueError

result = results["results"]["bindings"][0]

for key in result.keys():
    final_result[key] = result[key]["value"]

print(final_result)





