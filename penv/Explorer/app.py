from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# API keys
OPENWEATHER_API_KEY = 'e1dfe68316f95a406de29f3bc2930506'
MAPBOX_API_KEY = 'pk.eyJ1IjoibmF2ZWVuLS1yYWoiLCJhIjoiY20xOWVoZDcwMThmcjJqc2poamN2Y2U4OSJ9.zm8YN3h7sK9nAbh6XRAoFQ'
OPENTRIPMAP_API_KEY = '5ae2e3f221c38a28845f05b68f83202fe7f7056bd2ee7bbe33e27ab5'  # Replace with your actual OpenTripMap API key
UNSPLASH_API_KEY = '2GzGE14fpGxRkMzE7sTIJz1UDTlASI8GAxAO5BmI8EQ'  # 

WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'
OPENTRIPMAP_API_URL = 'https://api.opentripmap.com/0.1/en/places'
UNSPLASH_API_URL = 'https://api.unsplash.com/search/photos'
MAPBOX_GEOCODING_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places'

# Popular destinations
POPULAR_DESTINATIONS = [
    "Paris, France",
    "Tokyo, Japan",
    "New York City, USA",
    "Rome, Italy",
    "Sydney, Australia",
    "London, UK",
    "Barcelona, Spain",
    "Dubai, UAE"
]

def get_place_details(destination):
    params = {
        'action': 'query',
        'format': 'json',
        'titles': destination,
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
        'redirects': 1
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    if response.status_code == 200:
        pages = response.json()['query']['pages']
        for page in pages.values():
            return page.get('extract', 'No summary available.')
    return 'No summary available.'

def get_weather(lat, lon):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(weather_url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_coordinates(destination):
    url = f"{MAPBOX_GEOCODING_URL}/{destination}.json"
    params = {
        'access_token': MAPBOX_API_KEY,
        'limit': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            return data['features'][0]['center']
    return None

def get_tourist_attractions(lat, lon, radius=10000):
    attractions_url = f"{OPENTRIPMAP_API_URL}/radius"
    params = {
        'radius': radius,
        'lon': lon,
        'lat': lat,
        'rate': '3',  # Minimum rating of 3 to get popular attractions
        'format': 'json',
        'limit': 15,  # Increased limit for broader areas
        'kinds': 'tourist_facilities,museums,architecture,cultural,historical_places,monuments_and_memorials,natural,amusements',
        'apikey': OPENTRIPMAP_API_KEY
    }
    response = requests.get(attractions_url, params=params)
    if response.status_code == 200:
        attractions = response.json()
        detailed_attractions = []
        for attraction in attractions:
            details_url = f"{OPENTRIPMAP_API_URL}/xid/{attraction['xid']}"
            details_params = {
                'apikey': OPENTRIPMAP_API_KEY
            }
            details_response = requests.get(details_url, params=details_params)
            if details_response.status_code == 200:
                details = details_response.json()
                detailed_attraction = {
                    'name': details.get('name', 'Unknown'),
                    'description': details.get('wikipedia_extracts', {}).get('text', 'No description available.'),
                    'image': details.get('preview', {}).get('source', ''),
                    'lat': details.get('point', {}).get('lat', attraction['point']['lat']),
                    'lon': details.get('point', {}).get('lon', attraction['point']['lon']),
                    'kinds': details.get('kinds', '').replace(',', ', ')
                }
                detailed_attractions.append(detailed_attraction)
        return detailed_attractions
    return []

def get_destination_images(destination):
    params = {
        'query': destination,
        'client_id': UNSPLASH_API_KEY,
        'per_page': 10,  # Increased to fetch more images
        'orientation': 'landscape'  # To get more suitable images for display
    }
    response = requests.get(UNSPLASH_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return [photo['urls']['regular'] for photo in data['results']]
    return []

@app.route('/')
def index():
    popular_destinations_with_images = []
    for destination in POPULAR_DESTINATIONS:
        images = get_destination_images(destination)
        popular_destinations_with_images.append({
            'name': destination,
            'image': images[0] if images else None
        })
    return render_template('index.html', popular_destinations=popular_destinations_with_images)

@app.route('/explore', methods=['POST', 'GET'])
def explore():
    if request.method == 'POST':
        destination = request.form['destination']
    else:
        destination = request.args.get('destination')
    
    coordinates = get_coordinates(destination)
    if coordinates:
        lng, lat = coordinates
        weather_data = get_weather(lat, lng)
        place_details = get_place_details(destination)
        
        # Adjust radius based on the type of destination
        if ',' in destination:  # Assuming it's a city
            attractions = get_tourist_attractions(lat, lng, radius=10000)
        else:  # Assuming it's a country or larger area
            attractions = get_tourist_attractions(lat, lng, radius=50000)
        
        destination_images = get_destination_images(destination)

        return render_template('details.html', 
                               destination=destination, 
                               weather_data=weather_data, 
                               lat=lat,
                               lng=lng,
                               place_details=place_details,
                               attractions=attractions,
                               destination_images=destination_images,
                               mapbox_api_key=MAPBOX_API_KEY)
    else:
        return "Location not found. Please try a different destination."

if __name__ == '__main__':
    app.run(debug=True)