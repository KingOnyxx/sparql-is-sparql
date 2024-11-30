from django.shortcuts import render
import requests

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
    