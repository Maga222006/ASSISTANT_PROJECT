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
        self.schema = {
            'type': 'function',
            'function': {
                'name': 'map',
                'description': 'Always use this function to display a location on the map. '
                               'Use it every time user asks for directions, how to get to a place, or requests to view/search/show/retrieve/display any location.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'location': {
                            'type': 'str',
                            'description': 'The exact name or address of the location to show on the map.'
                        }
                    },
                    'required': ['location'],
                },
            },
        }

    def run(self, location):
        return ToolResponse(
            tool="map",
            text=f"Searching {location}",
            location=location
        )
