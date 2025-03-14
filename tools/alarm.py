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
                'name': 'alarm',
                'description': 'Alarm function, sets an alarm for the specific time.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'time': {
                            'type': 'str',
                            'description': 'Alarm time in format HH:MM .'
                        }
                    },
                    'required': ['time'],
                },
            },
        }

    def run(self, time):
        """Set an alarm for the given time."""
        return ToolResponse(
            tool="alarm",
            text=time,
            alarm=time
        )
