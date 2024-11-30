from django.shortcuts import render
from rdflib import Graph, URIRef, Literal, Namespace
from SPARQLWrapper import SPARQLWrapper, JSON
from .airport_queries import airport_queries
from .country_queries import get_flag

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
        'id' : airport_id,
        'type': result["type"][27:].replace("_", " "),
        'name': result["name"],
        'ident': result["ident"],
        'iata_code': result["iata_code"],
        'gps_code': result["gps_code"],
        'scheduled_service': result["scheduled_service"],
        'municipality': result["municipality"][27:],
        'municipality_label': result["municipality_label"].replace("_", " "),
        'iso_region': result["iso_region"][27:],
        'region_label': result["region_label"],
        'iso_country': result["iso_country"][27:],
        'country_label': result["country_label"],
        'continent': result["continent"][27:],
        'latitude_deg': result["latitude_deg"],
        'longitude_deg': result["longitude_deg"],
        'elevation_ft': result["elevation_ft"],
        'runways': result["runways"],
        'runway_ids': [runway[27:] for runway in result["runways"]],
        'runway_labels': result["runway_labels"],
        'navaids': result["navaids"],
        'navaid_ids': [navaid[27:] for navaid in result["navaids"]],
        'navaid_labels': result["navaid_labels"],
        'navaid_idents': result ["navaid_idents"]
    }

    paired_runways = zip(airport_data['runway_labels'], airport_data['runway_ids'])
    tripled_navaids = zip(airport_data['navaid_labels'], airport_data['navaid_ids'], airport_data['navaid_idents'])

    return render(request, 'airports_page.html', {'airport_data': airport_data, 'paired_runways': paired_runways, 
                                                  'tripled_navaids': tripled_navaids, 'page': {'title': 'Airport Details'}})




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




def navaid_view(request, navaid_id):
    # Example data for a navaid
    navaid_data = {
        'id': 'N123',
        'ident': 'VOR1',
        'name': 'VOR Station 1',
        'type': 'VOR',
        'frequency_khz': '115.9',
        'latitude_deg': '33.5',
        'longitude_deg': '-118.5',
        'elevation_ft': '450',
        'iso_country': 'US',
        'magnetic_variation_deg': '5.2',
        'usageType': 'Commercial',
        'power': '50 Watts',
        'associated_airport': 'LAX'
    }
    return render(request, 'navaids_page.html', {'navaid_data': navaid_data, 'page': {'title': 'Navaid Details'}})



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





def runway_view(request, runway_id):
    # Example data for a runway
    runway_data = {
        'id': 'RW123',
        'airport_ref': 'LAX',
        'airport_ident': 'LAX Runway 1',
        'length_ft': '12000',
        'width_ft': '200',
        'surface': 'Asphalt',
        'lighted': 'Yes',
        'closed': 'No',
        'le_ident': 'RWY1'
    }
    return render(request, 'runways_page.html', {'runway_data': runway_data, 'page': {'title': 'Runway Details'}})
