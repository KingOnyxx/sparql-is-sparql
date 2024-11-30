from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
from .airport_queries import airport_queries
from .country_queries import get_flag, cotw_queries
from .navaid_queries import navaid_queries
from .runway_queries import runway_queries
from .search_queries import search_queries
from .region_queries import region_queries
from django.shortcuts import render

# punya joel
# SPARQL = SPARQLWrapper("http://DESKTOP-V5G8723:7200/repositories/airports")

# punya adrial
SPARQL = SPARQLWrapper("http://DESKTOP-CMK0990:7200/repositories/airport")
WIKIDATA_SPARQL = 'https://query.wikidata.org/sparql'

def results_view(request):
    query = request.GET.get('query', '')
    result = search_queries(query, SPARQL)
    print(result)
    # Get data for airports and labels
    results_data = {
        'airports': [airport[27:] for airport in result.get("airports", [])],
        'airport_labels': [label for label in result.get("airport_labels", [])]
    }

    # Pair the airport names with their labels
    paired_airports = zip(results_data['airports'], results_data['airport_labels'])
    # print(results_data['airports'])
    # print(results_data['airport_labels'])
    

    return render(request, 'results_page.html', {
        'results_data': results_data,
        'paired_airports': paired_airports,
        'page': {'title': 'Search Results'}
    })







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
    # Get the flag URL using the get_flag function
    flag_url = get_flag(iso_country, WIKIDATA_SPARQL)


    # Example data fetching (replace with actual SPARQL queries using cotw_queries)
    try:
        result = cotw_queries(iso_country, SPARQL)
    except ValueError:
        result = {}

    # Populate the country data dynamically
    country_data = {
        'code': iso_country,
        'name': result.get("label", ""),
        'continent': result.get("continentCode", ""),
        # 'continent_label': result.get("continentCode", "")[27:],
        'airports': result.get("airports", ""),
        'airports_labels': result.get("airports_labels", ""),

        ######################### masih belom ##############################
        'regions_contained': result.get("regions_contained", ""),
        'regions_contained_labels': result.get("regions_contained_labels", ""),
        ####################################################################

        'region_is_contained_in': result.get("Region", ""),
        'region_is_contained_in_label': result.get("Region", "")[29:],
        'region': result.get("Region", ""),
        'population': result.get("Population", ""),
        'area': result.get("AreaInSquareMiles", ""),
        'pop_density': result.get("PopulationDensityPerSquareMiles", ""),
        'coastline': result.get("CoastlineRatio", ""),
        'net_migration': result.get("NetMigration", ""),
        'infant_mortality': result.get("InfantMortality", ""),
        'gdp': result.get("GDPInUSD", ""),
        'literacy': result.get("LiteracyRate", ""),
        'phones': result.get("Phones", ""),
        'arable': result.get("arablePercentage", ""),
        'crops': result.get("cropsPercentage", ""),
        'other': result.get("othersPercentage", ""),
        'climate': result.get("Climate", ""),
        'birthrate': result.get("Birthrate", ""),
        'deathrate': result.get("Deathrate", ""),
        'agriculture': result.get("AgricultureRatio", ""),
        'industry': result.get("IndustryRatio", ""),
        'service': result.get("ServiceRatio", "")
    }

    airports = [
        {
            "label": label,
            "id": airport.split("/")[-1] 
        }
        for label, airport in zip(country_data['airports_labels'], country_data['airports'])
    ]

    regions = [
        {
            "label": label,
            "id": region.split("/")[-1] 
        }
        for label, region in zip(country_data['regions_contained_labels'], country_data['regions_contained'])
    ]
    print(regions)

    return render(
        request,
        'countries_page.html',
        {
            'country_data': country_data,
            'page': {'title': 'Country Details'},
            'flag_url': flag_url,
            'airports_list': airports,
            'regions_list': regions
        }
    )








def region_view(request, region_id):
    results = region_queries(region_id, SPARQL)

    print(results)
    region_data = {
        'id': results.get("region", "")[27:],
        'code': results.get("hasID", "")[27:]   ,
        'local_code': results.get("hasLocalCode", ""),
        'name': results.get("label", ""),
        # 'continent': results.get("continent", "")[27:],
        'iso_country': results.get("country", "")[27:],
        'country_label': results.get("labelCountry", "")
        # 'airports': results.get("airports", [])
    }
    # Example data for a region
    # region_data = {
    #     'id': 'R123',
    #     'code': 'R001',
    #     'local_code': 'RC1',
    #     'name': 'North America',
    #     'continent': 'North America',
    #     'iso_country': 'US',
    #     'airports': 'Multiple Airports'
    # }
    return render(request, 'regions_page.html', {'region_data': region_data, 'page': {'title': 'Region Details'}})