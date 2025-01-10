import datetime
import os
from geopy import Nominatim
from semantic_router import Route
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
        self.route = Route(
            name="current_time",
            utterances=[
                "what time is it"
                "what date is it today"
                "tell me what is the time",
                "what is the date ",
                "time in warshaw",
                "date",
                "what date is it today",
                "time in ny",
                "what is the time and date in boston",
                "time",
                "what is the time in makhachkala",
                "date time in st petersburg",
                "what's the date in vienna",
                "date time",
            ],
        )
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
        """Get the current time for a location or current position."""
        location_data = self.geolocator.geocode(location) if location else self.geolocator.geocode(os.getenv('LOCATION'))
        timezone = pytz.timezone(self.tf.timezone_at(lat=location_data.latitude, lng=location_data.longitude))
        return ToolResponse(
            tool="current_time",
            text=f"Location: {location.capitalize() if location else os.getenv('LOCATION')}; Current Date and Time: {datetime.datetime.now(timezone).strftime('%Y-%m-%d %H:%M')}, {self.weekday_mapping[datetime.datetime.now().weekday()]}."
        )
