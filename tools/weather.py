import datetime
import requests
import os
import logging
from geopy.geocoders import Nominatim
from model import Generator
from dotenv import load_dotenv
load_dotenv()

class ToolResponse:
    def __init__(self, tool, text=None, error=None, link=None, location=None, alarm=None, timer=None, stopwatch=None):
        self.tool = tool
        self.text = text
        self.error = error
        self.link = link
        self.location = location
        self.alarm = alarm
        self.timer = timer
        self.stopwatch = stopwatch

class Tool:
    def __init__(self):
        self.generator = Generator()
        self.call_llm = self.generator.call_llm
        self.geolocator = Nominatim(user_agent="my_geocoder")
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')

        if not self.api_key:
            logging.warning("OpenWeatherMap API key not found")
        self.schema = {
            'type': 'function',
            'function': {
                'name': 'weather',
                'description': 'Get the weather forecast for the week or several days. '
                               'Use it to search weather forecast for the location, city, place, etc. '
                               'Use every time user asks about current weather or forecast regardless how many times. ',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'location': {
                            'type': 'str',
                            'description': "The location, i.e city, village, country, etc. "
                                           "By default None (location will be determined automatically). ",
                        },
                    },
                }
            }}

    def _get_weather_data(self, lat: float, lon: float) -> list:
        """Fetch weather data from OpenWeatherMap API."""
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not configured")

        units = os.getenv("UNITS", "metric")
        unit_symbol = {'metric': 'C', 'imperial': 'F', 'standard': 'K'}[units]

        response = requests.get(
            'https://api.openweathermap.org/data/2.5/forecast',
            params={
                'lat': lat,
                'lon': lon,
                'units': units,
                'appid': self.api_key
            },
            timeout=10
        ).json()

        days = []
        today = datetime.datetime.now()
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for i, label in enumerate(['today', 'tomorrow'] + [f'in {i} days' for i in range(2, 6)]):
            date = today + datetime.timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')

            # For today, get the next available forecast
            if label == 'today':
                forecast = next(
                    (item for item in response['list'] if
                     datetime.datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S') >= today),
                    None
                )
            else:
                # For other days, get the forecast around noon
                forecast = next(
                    (item for item in response['list'] if date_str in item['dt_txt'] and '15:00:00' in item['dt_txt']),
                    next((item for item in response['list'] if date_str in item['dt_txt']), None)
                )

            if forecast:
                days.append([
                    label,
                    date_str,
                    weekdays[date.weekday()],
                    forecast['weather'][0]['description'],
                    forecast['main']['temp'],
                    unit_symbol
                ])

        return days

    def run(self, location=None) -> ToolResponse | ToolResponse:
        """Get weather forecast for a location or current position."""
        try:
            if location:
                loc_data = self.geolocator.geocode(location)
                if loc_data:
                    coords = (loc_data.latitude, loc_data.longitude)
            else:
                loc_data = self.geolocator.geocode(os.getenv('LOCATION'))
                if loc_data:
                    coords = (loc_data.latitude, loc_data.longitude)
                if not coords:
                    return ToolResponse(
                        tool='weather',
                        error='Was not able to parse the coordinates.'
                    )
            forecast = self._get_weather_data(*coords)
            return ToolResponse(
                tool='weather',
                text='; '.join(' '.join(str(item) for item in day) for day in forecast)
            )
        except Exception as e:
            logging.error(f"Weather error: {str(e)}")
            return ToolResponse(
                tool='weather',
                error=str(e)
            )
