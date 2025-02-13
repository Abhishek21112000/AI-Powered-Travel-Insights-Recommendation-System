
import requests
from datetime import datetime

# API Keys (replace with your actual keys)
OPENWEATHER_API_KEY = ""
GOOGLE_MAPS_API_KEY = ""
YELP_API_KEY = ""


def get_travel_time(origin, destination):
    """ Fetch travel time between two locations using Google Maps API. """
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "mode": "driving",
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200 and data["status"] == "OK":
        try:
            duration = data["rows"][0]["elements"][0]["duration"]["text"]
            return duration
        except (IndexError, KeyError):
            return "Travel time unavailable"
    else:
        return "Error fetching travel time"


def get_weather_forecast(city, start_date, end_date):
    """ Fetch weather forecast for a city during a given date range. """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=imperial"
    response = requests.get(url).json()

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    forecast = {}
    for day in response['list']:
        forecast_date = datetime.strptime(day['dt_txt'], "%Y-%m-%d %H:%M:%S").date()
        if start_date <= forecast_date <= end_date:
            temp_f = day['main']['temp']
            temp_c = (temp_f - 32) / 1.8  # Convert to Celsius
            condition = day['weather'][0]['description']

            if forecast_date not in forecast:
                forecast[forecast_date] = {"description": condition, "temperature": temp_c}

    return {
        "start_date": forecast.get(start_date, {"description": "No data", "temperature": 0}),
        "return_date": forecast.get(end_date, {"description": "No data", "temperature": 0}),
    }


def get_attractions(destination):
    """ Fetch top attractions for a city using Yelp API. """
    base_url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {
        "location": destination,
        "term": "attractions",
        "sort_by": "rating",
        "limit": 5
    }
    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200:
        try:
            return [biz["name"] for biz in data["businesses"]]
        except KeyError:
            return ["No attractions found"]
    else:
        return ["Error fetching attractions"]


def get_hotels(destination):
    """ Fetch top hotel suggestions for a city using Yelp API. """
    base_url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {
        "location": destination,
        "term": "hotels",
        "sort_by": "rating",
        "limit": 5
    }
    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200:
        try:
            return [biz["name"] for biz in data["businesses"]]
        except KeyError:
            return ["No hotels found"]
    else:
        return ["Error fetching hotels"]


def get_local_insights(destination):
    """ Fetch local insights such as food places, photography spots, and travel tips using Yelp API. """
    base_url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

    insights = {}

    # Fetch food recommendations
    params = {"location": destination, "term": "food", "sort_by": "rating", "limit": 3}
    response = requests.get(base_url, headers=headers, params=params)
    insights["food"] = [biz["name"] for biz in response.json().get("businesses", [])]

    # Fetch best photography spots
    params["term"] = "photography spots"
    response = requests.get(base_url, headers=headers, params=params)
    insights["photography"] = [biz["name"] for biz in response.json().get("businesses", [])]

    # Fetch general local travel tips (using "travel" category)
    params["term"] = "travel tips"
    response = requests.get(base_url, headers=headers, params=params)
    insights["tips"] = [biz["name"] for biz in response.json().get("businesses", [])]

    return insights


def generate_packing_list(weather):
    """ Generate a packing list based on weather conditions. """
    packing_list = ["Clothes", "Toiletries", "Travel Documents"]
    weather_items = {
        "rain": ["Raincoat", "Waterproof Shoes", "Umbrella"],
        "snow": ["Warm Clothes", "Gloves", "Scarf", "Boots"],
        "sunny": ["Sunglasses", "Hat", "Sunscreen"],
        "clear": ["Sunglasses", "Hat", "Sunscreen"]
    }
    temp_items = [
        (0, ["Thermal Underwear", "Heavy Coat"]),
        (10, ["Sweater", "Jacket"]),
        (20, ["Light Jacket"]),
        (30, ["Light Clothing", "Water Bottle", "Cooling Towel"])
    ]

    def add_weather_items(description):
        for key in weather_items:
            if key in description:
                packing_list.extend(weather_items[key])
                break

    def add_temp_items(temperature):
        for temp, items in temp_items:
            if temperature < temp:
                packing_list.extend(items)
                break
        else:
            if temperature >= 30:
                packing_list.extend(temp_items[-1][1])

    if isinstance(weather, dict) and "description" in weather and "temperature" in weather:
        add_weather_items(weather["description"].lower())
        add_temp_items(weather["temperature"])
    elif isinstance(weather, str):
        add_weather_items(weather.lower())
    else:
        raise ValueError("Invalid weather data format")

    return packing_list
