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
                  'description': 'Get the current time and date for the location, city, place, etc.'
                                 'Use every time user asks about current time regardless how many times.',
                  'parameters': {
                      'type': 'object',
                      'properties': {
                          'location': {
                              'type': 'str',
                              'description': 'The location, i.e city, village, country, etc.'
                                             'By default None (searches the time for user location)',
                          },
                      },
                  }
              }}

    def run(self, location=None):
        location_data = self.geolocator.geocode(location) if location else self.geolocator.geocode(os.getenv('LOCATION'))
        timezone = pytz.timezone(self.tf.timezone_at(lat=location_data.latitude, lng=location_data.longitude))
        return ToolResponse(
            tool="current_time",
            text=f"Current date and time for {location.upper() if location else os.getenv('LOCATION')}: {datetime.datetime.now(timezone).strftime('%Y-%m-%d %H:%M')}, {self.weekday_mapping[datetime.datetime.now().weekday()]}."
        )
