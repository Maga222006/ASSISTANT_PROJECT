import datetime
import os
from geopy import Nominatim
from timezonefinder import TimezoneFinder
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
                      'required': ['location'],
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
