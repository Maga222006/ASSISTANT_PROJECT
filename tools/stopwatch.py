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
                'name': 'stopwatch',
                'description': 'Stopwatch function, starts/stops the stopwatch.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'action': {
                            'type': 'str',
                            'description': 'One of the two commands start/stop the stopwatch.',
                            'enum': ["start", "stop"]
                        }
                    },
                    'required': ['action'],
                },
            },
        }

    def run(self, action):
        return ToolResponse(
            tool="stopwatch",
            text=f"Stopwatch {action}: success",
            stopwatch=action
        )
