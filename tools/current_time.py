import datetime
import os
from geopy import Nominatim
from timezonefinder import TimezoneFinder
from model import Generator
import pytz

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
        self.tf = TimezoneFinder()
        self.geolocator = Nominatim(user_agent="my_geocoder")
        self.weekday_mapping = ("Monday", "Tuesday",
                                "Wednesday", "Thursday",
                                "Friday", "Saturday",
                                "Sunday")

        self.schema = {
            'type': 'function',
            'function': {
                'name': 'current_time',
                'description': 'Always use this function to get the current time and date for a specified location. '
                               'Use it every time user asks about the current time, regardless of how often they ask.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'location': {
                            'type': 'str',
                            'description': 'The name of the location, such as a city, village, or country. Defaults to None, which retrieves the current time for the user\'s location.',
                        },
                    },
                }
            }
        }

    def run(self, location=None):
        location_data = self.geolocator.geocode(location) if location else self.geolocator.geocode(os.getenv('LOCATION'))
        timezone = pytz.timezone(self.tf.timezone_at(lat=location_data.latitude, lng=location_data.longitude))
        return ToolResponse(
            tool="current_time",
            text=f"Location: {location.capitalize() if location else os.getenv('LOCATION')}; Current Date and Time: {datetime.datetime.now(timezone).strftime('%Y-%m-%d %H:%M')}, {self.weekday_mapping[datetime.datetime.now().weekday()]}."
        )
