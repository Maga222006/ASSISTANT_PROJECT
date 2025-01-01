class ToolResponse:
    def __init__(self, tool, text=None, error=None, link=None, image=None):
        self.tool = tool
        self.text = text
        self.error = error
        self.link = link
        self.image = image

class Tool:
    def __init__(self, ):
        self.schema = {
            'type': 'function',
            'function': {
                'name': 'timer',
                'description': 'Timer function, starts timer for hours, minutes or seconds'
                               'Be very careful with each parameter',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'hours': {
                            'type': 'int',
                            'description': 'The offset in hours / h'
                                           'Do not confuse with minutes / mins or seconds / secs'
                                           'By default 0',
                        },
                        'minutes': {
                            'type': 'int',
                            'description': 'The offset in minutes / min / mins'
                                           'Do not confuse with hours / h or seconds / secs'
                                           'By default 0',
                        },
                        'seconds': {
                            'type': 'int',
                            'description': 'The offset in seconds / sec / secs'
                                           'Do not confuse with minutes / mins or hours / h'
                                           'By default 0',
                        },

                    },
                },
            },
        }

    def run(self, hours=0, minutes=0, seconds=0):
        return ToolResponse(
            tool="timer",
            text=f"The timer has been set. Timer link: http://www.google.com/search?q=timer+for+{hours}+hours+{minutes}+minutes+{seconds}+seconds",
            link=f"http://www.google.com/search?q=timer+for+{hours}+hours+{minutes}+minutes+{seconds}+seconds"
        )
