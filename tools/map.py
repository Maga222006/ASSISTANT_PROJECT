from semantic_router import Route


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
    def __init__(self, ):
        self.route = Route(
            name="map",
            utterances=[
                "show me on the map",
                "open the map",
                "build an itinerary",
                "show me where is"
                "give me the route"
            ],
        )
        self.schema = {
            'type': 'function',
            'function': {
                'name': 'map',
                'description': 'Open the location in the map'
                               'Use every time user asks for directions, how to get somwhere or to show something on the map',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'location': {
                            'type': 'str',
                            'description': 'Location name'
                        }
                    },
                    'required': ['location'],
                },
            },
        }

    def run(self, location):
        """Display the location on the map."""
        return ToolResponse(
            tool="map",
            text=f"Searching {location}",
            location=location
        )
