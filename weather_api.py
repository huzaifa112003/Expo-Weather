# to import api 
import requests

API_KEY = 'c365626736cd1efcc0e69bdb55b50154'
BASE_URL_WEATHER = 'http://api.openweathermap.org/data/2.5/weather?'
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast?'

def get_current_weather(city_name):
    current_weather_url = f"{BASE_URL_WEATHER}q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(current_weather_url)
    if response.status_code == 200:
        data = response.json()
        # Check if 'name' is in the response to validate it's a proper city
        if 'name' in data and data.get('cod') == 200:
            return data
        else:
            return None
    else:
        return None

    
def get_weather_forecast(city_name):
    """Fetch weather forecast data for a given city."""
    url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns the forecast data as a Python dictionary
    else:
        return None