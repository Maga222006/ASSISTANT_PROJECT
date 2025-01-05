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
                'name': 'timer',
                'description': 'Timer function, starts timer for hours, minutes or seconds.'
                               'Be very careful with each parameter.'
                               'Use only when you need to set a timer.'
                               'Do not use this tool to retrieve the current time anywhere, use "current_time" tool instead',
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
            text=f"{hours} hours, {minutes} minutes, {seconds} seconds.",
            timer=hours*3600+minutes*60+seconds
        )
        
