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
                'description': 'Always use this function to control the stopwatch. Use it whenever the user asks to start or stop a stopwatch, ensuring precise tracking of time.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'action': {
                            'type': 'str',
                            'description': 'Specify whether to start or stop the stopwatch. Accepted values are "start" or "stop".',
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
            text=action,
            stopwatch=action
        )
