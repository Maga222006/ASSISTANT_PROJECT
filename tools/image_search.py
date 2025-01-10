from duckduckgo_search import DDGS
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
    def __init__(self):
        self.route = Route(
            name="image_search",
            utterances=[
                "show me the image of",
                "what looks like",
                "retrieve me the picture of",
                "search for the photo of",
                "show me the photograph of",
                "find me an image of",
                "gimme the picture of"
            ],
        )
        self.schema = {
            'type': 'function',
            'function': {
                'name': 'image_search',
                'description': 'Search for an image with the user query.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'str',
                            'description': 'The text query for searching the image.',
                        },
                    },
                    'required': ['query'],
                }
            }}

    def run(self, query):
        """Get the image search results for the given query."""
        try:
            with DDGS() as ddgs:
                results = ddgs.images(query, max_results=1, safesearch='off')
            if results:
                return ToolResponse(
                    tool="image_search",
                    text="Images have been retrieved.",
                    link=results[0]['image']
                )
        except Exception as e:
            return ToolResponse(
                tool="image_search",
                error=f"An error occurred during the search: {e}"
            )

