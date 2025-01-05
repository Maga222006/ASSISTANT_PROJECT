from duckduckgo_search import DDGS

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
        self.schema = {
            'type': 'function',
            'function': {
                'name': 'image_search',
                'description': 'Always use this function to find images based on the user’s query. '
                               'Use it EVERY TIME user requests an image or asks to search/show/retrieve/display something visually.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'str',
                            'description': 'The keywords or phrase describing the image the user wants to find.',
                        },
                    },
                    'required': ['query'],
                }
            }
        }

    def run(self, query):
        try:
            with DDGS() as ddgs:
                results = ddgs.images(query, max_results=1, safesearch='off')
            if results:
                return ToolResponse(
                    tool="image_search",
                    text="Images retrieved.",
                    link=results[0]['image']
                )
        except Exception as e:
            return ToolResponse(
                tool="image_search",
                error=f"An error occurred during the search: {e}"
            )

