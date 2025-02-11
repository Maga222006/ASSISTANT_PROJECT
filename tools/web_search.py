from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WolframAlphaAPIWrapper, WikipediaAPIWrapper
from threading import Thread


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
        self.ddg = DuckDuckGoSearchAPIWrapper()
        self.wolfram = WolframAlphaAPIWrapper()
        self.wikipedia = WikipediaAPIWrapper()
        self.schema = {
            'type': 'function',
            'function': {
                'name': 'web_search',
                'description': 'Search information about current events, recent news, famous people, etc on the internet. '
                               'Do NOT search weather forecast or time with it, you have separate functions for that. ',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'The search query or question for browser. ',
                        },
                    },
                    'required': ['query'],
                },
            },
        }

    def run(self, query):
        """Get web search results for the given query."""
        result = {'wolfram alpha': '', 'web search': '', 'wikipedia': ''}

        def wiki_thread():
            result['wikipedia'] = self.wikipedia.run(query)

        def wolfram_thread():
            try:
                wolfram_result = self.wolfram.run(query)
            except:
                wolfram_result = None
            if wolfram_result and "Wolfram Alpha wasn't able to answer it" not in wolfram_result:
                result['wolfram alpha'] = wolfram_result

        def ddg_thread():
            result['web search'] = self.ddg.run(query)

        # Start the threads
        wikipedia_thread = Thread(target=wiki_thread)
        wolfram_thread = Thread(target=wolfram_thread)
        ddg_thread = Thread(target=ddg_thread)

        wikipedia_thread.start()
        wolfram_thread.start()
        ddg_thread.start()

        wikipedia_thread.join()
        wolfram_thread.join()
        ddg_thread.join()
        return ToolResponse(
            tool="web_search",
            text=result
        )
