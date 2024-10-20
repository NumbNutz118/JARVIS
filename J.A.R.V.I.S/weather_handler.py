import requests
from config import WEATHER_API_KEY, LOCATION

def get_weather(query=None):
    # WeatherAPI.com request URL (for current weather and forecast)
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q=West Haven, UT&days=2&aqi=no"
    
    
    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()
        current_condition = data['current']['condition']['text']
        current_temp_f = data['current']['temp_f']
        current_feels_like_f = data['current']['feelslike_f']
        current_wind_mph = data['current']['wind_mph']
        is_day = data['current']['is_day']
        location_name = data['location']['name']
        time = data['location']['localtime']

        # Get next day's forecast
        next_day_condition = data['forecast']['forecastday'][1]['day']['condition']['text']
        next_day_max_temp_f = data['forecast']['forecastday'][1]['day']['maxtemp_f']
        next_day_min_temp_f = data['forecast']['forecastday'][1]['day']['mintemp_f']

        # Customize response depending on weather conditions
        if is_day:
            time_of_day = "day"
        else:
            time_of_day = "night"
        
        # Create different responses based on the query
        if query == "temperature":
            return f"The current temperature in {location_name} is {current_temp_f}°F, but it feels like {current_feels_like_f}°F."
        elif query == "wind speed":
            return f"The current wind speed in {location_name} is {current_wind_mph} miles per hour."
        elif query == "condition":
            return f"The weather in {location_name} is currently {current_condition}."
        elif query == "full":
            return (f"The weather in {location_name} is currently {current_condition} with a temperature of {current_temp_f}°F, "
                    f"but it feels like {current_feels_like_f}°F. The wind speed is {current_wind_mph} miles per hour. It's {time}.")
        elif query == "next day":
            return (f"Tomorrow in {location_name}, the weather will be {next_day_condition} with a maximum temperature of "
                    f"{next_day_max_temp_f}°F and a minimum temperature of {next_day_min_temp_f}°F.")
        else:
            # Default response with full details
            return (f"The weather in {location_name} is currently {current_condition} with a temperature of {current_temp_f}°F, "
                    f"but it feels like {current_feels_like_f}°F. The wind speed is {current_wind_mph} miles per hour. It's {time_of_day} time. "
                    f"Tomorrow's weather will be {next_day_condition} with a high of {next_day_max_temp_f}°F and a low of {next_day_min_temp_f}°F.")

    except requests.exceptions.RequestException as e:
        return f"Sorry, I couldn't retrieve the weather information. Error: {e}"
