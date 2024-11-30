from django.shortcuts import render
import requests
from SPARQLWrapper import SPARQLWrapper, JSON

def get_flag(iso_country, wikidata_sparql):
    # Define the SPARQL endpoint for Wikidata

    # SPARQL query to get the flag image URL for Brunei using its ISO 2-digit code
    query = '''
    SELECT ?flag
    WHERE {
      ?country wdt:P31 wd:Q6256;  # Instance of country (Q6256)
               wdt:P297 "''' + iso_country + '''";  # ISO 2-digit code for the country
               wdt:P41 ?flag.  # Flag image (P41)
    }
    '''

    # Send the query to Wikidata's SPARQL endpoint
    response = requests.get(wikidata_sparql, params={'query': query, 'format': 'json'})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the response as JSON
        if data['results']['bindings']:
            flag_url = data['results']['bindings'][0]['flag']['value']
        else:
            flag_url = None
    else:
        flag_url = None

    return flag_url


def country_queries(id, sparql):
    print(type(id))
    print(id)
    final_result = dict()

    # Set the SPARQL query
    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX v: <http://myairports.com/vocab#>

    SELECT ?country ?label ?hasID ?partOf
    WHERE {
        ?country a v:country .
            OPTIONAL{ ?country rdfs:label ?label .}
            OPTIONAL{ ?country v:hasID ?hasID .}    
            OPTIONAL{ ?country v:partOf ?partOf .}
            FILTER()
            FILTER(?country = :""" + id + """ )
    }
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
    
    return(final_result)