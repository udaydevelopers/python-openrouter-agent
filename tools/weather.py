import requests


# ==================================================
# Open-Meteo APIs
# ==================================================

GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
)


# ==================================================
# Weather Code Description
# ==================================================

def get_weather_description(weather_code):

    weather_codes = {

        0: "Clear sky",

        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Depositing rime fog",

        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",

        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",

        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",

        66: "Light freezing rain",
        67: "Heavy freezing rain",

        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",

        77: "Snow grains",

        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",

        85: "Slight snow showers",
        86: "Heavy snow showers",

        95: "Thunderstorm",

        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    return weather_codes.get(
        weather_code,
        "Unknown weather condition"
    )


# ==================================================
# Find Location
# ==================================================

def find_location(city):

    params = {

        "name": city,

        "count": 1,

        "language": "en",

        "format": "json"
    }


    response = requests.get(

        GEOCODING_URL,

        params=params,

        timeout=10
    )


    response.raise_for_status()


    data = response.json()


    results = data.get("results", [])


    if not results:

        return None


    location = results[0]


    return {

        "name": location.get("name"),

        "country": location.get("country"),

        "latitude": location.get("latitude"),

        "longitude": location.get("longitude"),

        "timezone": location.get("timezone")
    }


# ==================================================
# Get Weather
# ==================================================

def get_weather(city):

    """
    Get current weather for a city.
    """

    # ----------------------------------------------
    # Find city coordinates
    # ----------------------------------------------

    location = find_location(city)


    if not location:

        return {

            "error":
                f"Could not find location: {city}"
        }


    # ----------------------------------------------
    # Weather parameters
    # ----------------------------------------------

    params = {

        "latitude":
            location["latitude"],

        "longitude":
            location["longitude"],

        "current": ",".join([

            "temperature_2m",

            "relative_humidity_2m",

            "apparent_temperature",

            "precipitation",

            "weather_code",

            "wind_speed_10m"

        ]),

        "timezone":
            "auto"
    }


    # ----------------------------------------------
    # Call Weather API
    # ----------------------------------------------

    response = requests.get(

        WEATHER_URL,

        params=params,

        timeout=10
    )


    response.raise_for_status()


    data = response.json()


    current = data.get(
        "current",
        {}
    )


    # ----------------------------------------------
    # Weather code
    # ----------------------------------------------

    weather_code = current.get(
        "weather_code"
    )


    description = get_weather_description(
        weather_code
    )


    # ----------------------------------------------
    # Return clean result
    # ----------------------------------------------

    return {

        "location":
            location["name"],

        "country":
            location["country"],

        "timezone":
            location["timezone"],

        "temperature_c":
            current.get(
                "temperature_2m"
            ),

        "feels_like_c":
            current.get(
                "apparent_temperature"
            ),

        "humidity_percent":
            current.get(
                "relative_humidity_2m"
            ),

        "precipitation_mm":
            current.get(
                "precipitation"
            ),

        "wind_speed_kmh":
            current.get(
                "wind_speed_10m"
            ),

        "weather_code":
            weather_code,

        "description":
            description,

        "observed_at":
            current.get(
                "time"
            )
    }