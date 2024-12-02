from collections import defaultdict
from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
from .airport_queries import airport_queries, get_all_airports
from .country_queries import get_all_countries, get_flag, cotw_queries
from .navaid_queries import navaid_queries
from .runway_queries import runway_queries
from .search_queries import search_queries
from .region_queries import region_queries
from django.shortcuts import render
from django.core.paginator import Paginator

SPARQL = SPARQLWrapper("http://localhost:7200/repositories/airports")
WIKIDATA_SPARQL = 'https://query.wikidata.org/sparql'

def results_view(request):
    query = request.GET.get('query', '')

    # Get sorting parameters
    sort_by = request.GET.get('sort', 'asc')
    page_numbers = {tab: int(request.GET.get(f'{tab.lower()}_page', 1)) for tab in ['Airports', 'Regions', 'Navaids', 'Runways', 'Countries']}

    # Fetch search results
    result = search_queries(query, SPARQL)

    # Prepare result data
    results_data = {
        'airports': [airport[27:] for airport in result.get("airports", [])],
        'airport_labels': [label for label in result.get("airport_labels", [])],
        'regions': [region[27:] for region in result.get("regions", [])],
        'region_labels': [label.replace("_", " ") for label in result.get("region_labels", [])],
        'navaids': [navaid[27:] for navaid in result.get("navaids", [])],
        'navaid_labels': [label for label in result.get("navaid_labels", [])],
        'runways': [runway[27:] for runway in result.get("runways", [])],
        'runway_labels': [label for label in result.get("runway_labels", [])],
        'countries': [country[27:] for country in result.get("countries", [])],
        'country_labels': [label for label in result.get("country_labels", [])],
    }

    # Pair and sort results
    def sort_results(paired):
        return sorted(paired, key=lambda x: x[1].lower(), reverse=(sort_by == 'desc'))

    paired_airports = sort_results(zip(results_data['airports'], results_data['airport_labels']))
    paired_regions = sort_results(zip(results_data['regions'], results_data['region_labels']))
    paired_navaids = sort_results(zip(results_data['navaids'], results_data['navaid_labels']))
    paired_runways = sort_results(zip(results_data['runways'], results_data['runway_labels']))
    paired_countries = sort_results(zip(results_data['countries'], results_data['country_labels']))

    # Create paginators
    paginated_airports = Paginator(paired_airports, 10).get_page(page_numbers['Airports'])
    paginated_regions = Paginator(paired_regions, 10).get_page(page_numbers['Regions'])
    paginated_navaids = Paginator(paired_navaids, 10).get_page(page_numbers['Navaids'])
    paginated_runways = Paginator(paired_runways, 10).get_page(page_numbers['Runways'])
    paginated_countries = Paginator(paired_countries, 10).get_page(page_numbers['Countries'])

    # Result counts
    result_counts = {
        'Airports': len(paired_airports),
        'Regions': len(paired_regions),
        'Navaids': len(paired_navaids),
        'Runways': len(paired_runways),
        'Countries': len(paired_countries),
    }

    # Sort tabs by result count
    sorted_tabs = sorted(result_counts.items(), key=lambda x: x[1], reverse=True)

    return render(request, 'results_page.html', {
        'query': query,
        'paginated_airports': paginated_airports,
        'paginated_regions': paginated_regions,
        'paginated_navaids': paginated_navaids,
        'paginated_runways': paginated_runways,
        'paginated_countries': paginated_countries,
        'result_counts': result_counts,
        'sorted_tabs': sorted_tabs,
        'sort_by': sort_by,
        'page': {'title': 'Search Results'},
    })






# View for Airport Details
def airport_view(request, airport_id):
    result = airport_queries(airport_id, SPARQL)

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

    # Precompute URLs for region and country
    region_url = f"/regions/{airport_data['iso_region']}" if airport_data['iso_region'] else None
    country_url = f"/countries/{airport_data['iso_country']}" if airport_data['iso_country'] else None

    # Grouped information with icons
    airport_info_groups = [
        {
            "category": "Basic Information",
            "items": [
                ("ID", airport_data["ident"], "🆔"),
                ("Type", airport_data["type"], "✈️"),
                ("Name", airport_data["name"], "📛"),
                ("IATA Code", airport_data["iata_code"], "🔠"),
                ("GPS Code", airport_data["gps_code"], "📡"),
                ("Local Code", airport_data["local_code"], "📍"),
            ]
        },
        {
            "category": "Location",
            "items": [
                ("Scheduled Service", airport_data["scheduled_service"], "🗓️"),
                ("Municipality", airport_data["municipality_label"], "🏙️"),
                ("Region", f'<a href="{region_url}" class="highlighted-cell">{airport_data["region_label"]}</a>' if region_url else "N/A", "📍"),
                ("Country", f'<a href="{country_url}" class="highlighted-cell">{airport_data["country_label"]}</a>' if country_url else "N/A", "🌍"),
                ("Continent", airport_data["continent"], "🌎"),
            ]
        },
        {
            "category": "Geographical Data",
            "items": [
                ("Latitude (deg)", airport_data["latitude_deg"], "📍"),
                ("Longitude (deg)", airport_data["longitude_deg"], "📍"),
                ("Elevation (ft)", airport_data["elevation_ft"], "⛰️"),
            ]
        },
    ]

    paired_runways = zip(airport_data['runway_labels'], airport_data['runway_ids'])
    tripled_navaids = zip(airport_data['navaid_labels'], airport_data['navaid_ids'], airport_data['navaid_idents'])

    return render(request, 'airports_page.html', {
        'airport_info_groups': airport_info_groups,
        'paired_runways': paired_runways,
        'tripled_navaids': tripled_navaids,
        'airport_data': airport_data,
        'page': {'title': 'Airport Details'}
    })




def navaid_view(request, navaid_id):
    result = navaid_queries(navaid_id, SPARQL)
    # print(result)
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
    """
    View for displaying detailed information about a country, including airports and regions.
    """
    # Get the flag URL
    flag_url = get_flag(iso_country, WIKIDATA_SPARQL)

    # Fetch data for the country using cotw_queries
    try:
        result = cotw_queries(iso_country, SPARQL)
    except ValueError:
        result = {}

    # Populate the country data dynamically
    country_data = {
        'code': iso_country,
        'name': result.get("label", ""),
        'continent': result.get("continentCode", ""),
        'region_is_contained_in': result.get("Region", ""),
        'region_is_contained_in_label': result.get("Region", "")[29:],
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

    # Define general information groups
    general_info_groups = [
        {
            "category": "Demographics",
            "items": [
                ("Population", country_data["population"], "👥"),
                ("Area", country_data["area"], "📐"),
                ("Population Density", country_data["pop_density"], "📊"),
            ]
        },
        {
            "category": "Agriculture",
            "items": [
                ("Arable", country_data["arable"], "🌾"),
                ("Crops", country_data["crops"], "🌽"),
                ("Other", country_data["other"], "🔍"),
            ]
        },
        {
            "category": "Economy",
            "items": [
                ("GDP", country_data["gdp"], "💰"),
                ("Agriculture", country_data["agriculture"], "🚜"),
                ("Industry", country_data["industry"], "🏭"),
                ("Service", country_data["service"], "🛠️"),
            ]
        },
        {
            "category": "Miscellaneous",
            "items": [
                ("Net Migration", country_data["net_migration"], "✈️"),
                ("Infant Mortality", country_data["infant_mortality"], "👶"),
                ("Literacy Rate", country_data["literacy"], "📖"),
                ("Phones", country_data["phones"], "📱"),
                ("Climate", country_data["climate"], "🌦️"),
                ("Birthrate", country_data["birthrate"], "🤱"),
                ("Deathrate", country_data["deathrate"], "⚰️"),
            ]
        },
    ]

    # Prepare airport data
    airport_data = [
        {"label": label, "id": airport.split("/")[-1]}
        for label, airport in zip(result.get("airports_labels", []), result.get("airports", []))
    ]

    # Sort and filter airport data
    sort_by_airport = request.GET.get("airport_sort", "label_asc")
    airport_items_per_page = int(request.GET.get("airport_items_per_page", 10))
    if sort_by_airport == "label_asc":
        airport_data.sort(key=lambda x: x["label"].lower())
    elif sort_by_airport == "label_desc":
        airport_data.sort(key=lambda x: x["label"].lower(), reverse=True)

    # Pagination for airports
    airport_page_number = request.GET.get("airport_page", 1)
    airport_paginator = Paginator(airport_data, airport_items_per_page)
    airports_page = airport_paginator.get_page(airport_page_number)

    # Prepare region data
    region_data = [
        {"label": label, "id": region.split("/")[-1]}
        for label, region in zip(result.get("regions_contained_labels", []), result.get("regions_contained", []))
    ]

    # Sort and filter region data
    sort_by_region = request.GET.get("region_sort", "label_asc")
    region_items_per_page = int(request.GET.get("region_items_per_page", 10))
    if sort_by_region == "label_asc":
        region_data.sort(key=lambda x: x["label"].lower())
    elif sort_by_region == "label_desc":
        region_data.sort(key=lambda x: x["label"].lower(), reverse=True)

    # Pagination for regions
    region_page_number = request.GET.get("region_page", 1)
    region_paginator = Paginator(region_data, region_items_per_page)
    regions_page = region_paginator.get_page(region_page_number)

    return render(
        request,
        'countries_page.html',
        {
            'country_data': country_data,
            'general_info_groups': general_info_groups,
            'page': {'title': f"Country Details: {country_data['name']}"},
            'flag_url': flag_url,
            'airports_page': airports_page,
            'regions_page': regions_page,
            'airport_sort': sort_by_airport,
            'airport_items_per_page': airport_items_per_page,
            'region_sort': sort_by_region,
            'region_items_per_page': region_items_per_page,
        }
    )











def region_view(request, region_id):
    results = region_queries(region_id, SPARQL)

    region_data = {
        'id': results.get("region", "")[27:],
        'code': results.get("hasID", "")[27:],
        'local_code': results.get("hasLocalCode", ""),
        'name': results.get("label", "").replace("_", " "),
        'iso_country': results.get("country", "")[27:],
        'country_label': results.get("labelCountry", "")
    }

    # Grouped data with icons
    region_info_groups = [
        {
            "category": "General Information",
            "items": [
                ("ID", region_data["id"], "📌"),
                ("Code", region_data["code"], "🔢"),
                ("Local Code", region_data["local_code"], "🏷️"),
                ("Name", region_data["name"], "📛"),
            ]
        },
        {
            "category": "Country Information",
            "items": [
                ("ISO Country", f'<a href="/countries/{region_data["iso_country"]}" class="highlighted-cell">{region_data["country_label"]}</a>', "🌍"),
            ]
        }
    ]

    return render(
        request,
        'regions_page.html',
        {
            'region_info_groups': region_info_groups,
            'region_data': region_data,
            'page': {'title': 'Region Details'}
        }
    )



def all_airports(request):
    result = get_all_airports(SPARQL)

    # Retrieve airport data
    airport_data = result.get("airports", [])
    countries = sorted({airport["country"] for airport in airport_data})

    # Get sorting and filter parameters
    sort_by = request.GET.get("sort", "default")
    selected_country = request.GET.get("country", None)
    items_per_page = int(request.GET.get("items_per_page", 10))
    page_number = request.GET.get("page", 1)

    # Filter by country
    if selected_country:
        airport_data = [airport for airport in airport_data if airport["country"] == selected_country]

    # Apply sorting
    if sort_by == "label_asc":
        airport_data.sort(key=lambda x: x["label"].lower())
    elif sort_by == "label_desc":
        airport_data.sort(key=lambda x: x["label"].lower(), reverse=True)
    elif sort_by == "country_asc":
        airport_data.sort(key=lambda x: x["country"].lower())
    elif sort_by == "country_desc":
        airport_data.sort(key=lambda x: x["country"].lower(), reverse=True)

    # Pagination
    paginator = Paginator(airport_data, items_per_page)
    airports_page = paginator.get_page(page_number)

    return render(
        request,
        'all_airports.html',
        {
            'airports_page': airports_page,
            'countries': countries,
            'selected_country': selected_country,
            'sort_by': sort_by,
            'items_per_page': items_per_page,
        }
    )



def all_countries(request):
    """
    Retrieves all countries and implements pagination, sorting, and alphabetical categorization.
    """
    # Simulate fetching SPARQL data
    result = get_all_countries(SPARQL)

    # Extract country data
    countries = {
        'countries_code': result.get("countries_code", []),
        'countries_labels': result.get("countries_labels", [])
    }

    # Prepare country data
    country_data = [
        {"label": label, "code": code.split("/")[-1]}  # Extract ISO code
        for label, code in zip(countries["countries_labels"], countries["countries_code"])
    ]

    # Get sorting parameters
    sort_by = request.GET.get("sort", "default")  # Default to unsorted

    # Apply sorting
    if sort_by == "label_asc":
        country_data.sort(key=lambda x: x["label"].lower())
    elif sort_by == "label_desc":
        country_data.sort(key=lambda x: x["label"].lower(), reverse=True)

    # Alphabetical categorization
    alphabetized_countries = defaultdict(list)
    for country in country_data:
        first_letter = country["label"][0].upper()
        alphabetized_countries[first_letter].append(country)

    # Pagination
    items_per_page = int(request.GET.get("items_per_page", 10))
    country_page_number = request.GET.get("country_page", 1)
    country_paginator = Paginator(country_data, items_per_page)
    country_page = country_paginator.get_page(country_page_number)

    return render(
        request,
        'all_countries.html',
        {
            'country_page': country_page,
            'items_per_page': items_per_page,
            'sort_by': sort_by,
            'alphabetized_countries': dict(alphabetized_countries),
        }
    )

