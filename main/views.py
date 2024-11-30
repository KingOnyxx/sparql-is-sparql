from django.shortcuts import render
from rdflib import Graph, URIRef, Literal, Namespace
from SPARQLWrapper import SPARQLWrapper, JSON
from .airport_queries import airport_queries
from .country_queries import get_flag
from .navaid_queries import navaid_queries
from .runway_queries import runway_queries

SPARQL = SPARQLWrapper("http://DESKTOP-V5G8723:7200/repositories/airports")
WIKIDATA_SPARQL = 'https://query.wikidata.org/sparql'

# Create your views here.

def home(request):
    return render(request, 'index.html')


def search(request):
    if request.method == "GET":
        # search = request.GET.get('search')
        # print(search)
        query = ""
    return True
    



from django.shortcuts import render



from django.shortcuts import render

# View for Airport Details
def airport_view(request, airport_id):
    result = airport_queries(airport_id, SPARQL)
    print(result)

    # Example airport data (replace with actual data)
    airport_data = {
    'id': airport_id,
    'type': result.get("type", "")[27:].replace("_", " ") if result.get("type", "") else "",
    'name': result.get("name", ""),
    'ident': result.get("ident", ""),
    'iata_code': result.get("iata_code", ""),
    'gps_code': result.get("gps_code", ""),
    'local_code': result.get("local_code", ""),
    'scheduled_service': result.get("scheduled_service", ""),
    'municipality': result.get("municipality", "")[27:] if result.get("municipality", "") else "",
    'municipality_label': result.get("municipality_label", "").replace("_", " "),
    'iso_region': result.get("iso_region", "")[27:] if result.get("iso_region", "") else "",
    'region_label': result.get("region_label", ""),
    'iso_country': result.get("iso_country", "")[27:] if result.get("iso_country", "") else "",
    'country_label': result.get("country_label", ""),
    'continent': result.get("continent", "")[27:] if result.get("continent", "") else "",
    'latitude_deg': result.get("latitude_deg", ""),
    'longitude_deg': result.get("longitude_deg", ""),
    'elevation_ft': result.get("elevation_ft", ""),
    'runways': result.get("runways", []),
    'runway_ids': [runway[27:] for runway in result.get("runways", [])],
    'runway_labels': result.get("runway_labels", []),
    'navaids': result.get("navaids", []),
    'navaid_ids': [navaid[27:] for navaid in result.get("navaids", [])],
    'navaid_labels': result.get("navaid_labels", []),
    'navaid_idents': result.get("navaid_idents", [])
    }

    paired_runways = zip(airport_data['runway_labels'], airport_data['runway_ids'])
    tripled_navaids = zip(airport_data['navaid_labels'], airport_data['navaid_ids'], airport_data['navaid_idents'])

    return render(request, 'airports_page.html', {'airport_data': airport_data, 'paired_runways': paired_runways, 
                                                  'tripled_navaids': tripled_navaids, 'page': {'title': 'Airport Details'}})


def navaid_view(request, navaid_id):
    result = navaid_queries(navaid_id, SPARQL)
    print(result)
    # Example data for a navaid
    
    navaid_data = {
    'id': result.get("navaid", "")[27:],
    'ident': result.get("ident", ""),
    'name': result.get("name", ""),
    'type': result.get("type", "")[27:],
    'frequency_khz': result.get("frequency_khz", ""),
    'latitude_deg': result.get("latitude_deg", ""),
    'longitude_deg': result.get("longitude_deg", ""),
    'elevation_ft': result.get("elevation_ft", ""),
    'iso_country': result.get("iso_country", "")[27:],
    'magnetic_variation_deg': result.get("magnetic_variation_deg", ""),
    'usageType': result.get("usage_type", "")[27:],
    'power': result.get("power", "")[27:],
    'airport_id': result.get("airport_id", ""),
    'associated_airport': result.get("airport", "")[27:],
    'airport_label': result.get("airport_label", "")
    }

    print(navaid_data["airport_id"])
    return render(request, 'navaids_page.html', {'navaid_data': navaid_data, 'page': {'title': 'Navaid Details'}})


def runway_view(request, runway_id):
    result = runway_queries(runway_id, SPARQL)

    runway_data = {
        'id': runway_id[7:],
        'runway': result.get("runway", ""),
        'airport': result.get("airport", "")[27:],
        'airport_label': result.get("airport_label", ""),
        'length_ft': result.get("length_ft", "")[:-3],
        'width_ft': result.get("width_ft", "")[:-3],
        'surface': result.get("surface", "")[27:],
        'lighted': result.get("isLighted", ""),
        'closed': result.get("isClosed", ""),
        'le_ident': result.get("leID", "")
    }
    return render(request, 'runways_page.html', {'runway_data': runway_data, 'page': {'title': 'Runway Details'}})



def country_view(request, iso_country):
    flag_url = get_flag(iso_country, WIKIDATA_SPARQL)
    
    # Example data for a country
    country_data = {
        'code': 'US',
        'name': 'United States',
        'continent': 'North America',
        'airports': 'Airports in US',
        'regions_contained': 'Northeast, West Coast',
        'region_is_contained_in': 'America',
        'population': '331000000',
        'area': '9833520',
        'pop_density': '33.5',
        'coastline': '190000',
        'net_migration': '0.5',
        'infant_mortality': '5.6',
        'gdp': '21137518',
        'literacy': '99%',
        'phones': '120',
        'arable': '15%',
        'crops': 'Wheat, Corn, Rice',
        'other': 'Timber, Oil',
        'climate': 'Varied',
        'birthrate': '12.4',
        'deathrate': '8.3',
        'agriculture': '5%',
        'industry': '30%',
        'service': '65%'
    }
    return render(request, 'countries_page.html', {'country_data': country_data, 'page': {'title': 'Country Details'}, 'flag_url': flag_url})








def region_view(request, region_id):
    # Example data for a region
    region_data = {
        'id': 'R123',
        'code': 'R001',
        'local_code': 'RC1',
        'name': 'North America',
        'continent': 'North America',
        'iso_country': 'US',
        'airports': 'Multiple Airports'
    }
    return render(request, 'regions_page.html', {'region_data': region_data, 'page': {'title': 'Region Details'}})