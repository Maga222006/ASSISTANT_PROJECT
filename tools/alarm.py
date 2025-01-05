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
                'description': 'Always use this function to set an alarm. '
                               'Use it EVERY TIME user requests to set an alarm for a specific time.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'time': {
                            'type': 'str',
                            'description': 'The exact time for the alarm in HH:MM format (24-hour clock).'
                        }
                    },
                    'required': ['time'],
                },
            },
        }

    def run(self, time):
        return ToolResponse(
            tool="alarm",
            text=time,
            alarm=time
        )
