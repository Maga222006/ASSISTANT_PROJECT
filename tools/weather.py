from langchain_community.utilities import WolframAlphaAPIWrapper
from dotenv import load_dotenv
from threading import Thread
import datetime
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
        self.wolfram = WolframAlphaAPIWrapper()
        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.prompts = [
            f"Today forecast for ",
            f"Tomorrow forecast for ",
            f"In 2 days forecast for ",
            f"In 3 days forecast for ",
            f"In 4 days forecast for ",
            f"In 5 days forecast for ",
        ]
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
                    'required': ['location'],
                }
            }
        }

    def run(self, location):
        forecast = []
        threads = []
        today = datetime.datetime.now()

        def retrieve_day(prompt):
            nonlocal location
            n = self.prompts.index(prompt)
            date = today + datetime.timedelta(days=n)
            date_str = date.strftime('%Y-%m-%d')
            forecast.append(f"{date_str} | {self.weekdays[date.weekday()]} | {self.wolfram.run(prompt+location)}")

        for prompt in self.prompts:
            thread = Thread(
                target=retrieve_day,
                args=(prompt,)
            )
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        try:
            return ToolResponse(
                tool="weather",
                text=f"Location: {location}; Forecast: {'; '.join(forecast)}."
            )
        except Exception as e:
            return ToolResponse(
                tool="weather",
                error=e
            )

