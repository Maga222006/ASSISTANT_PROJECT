from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WolframAlphaAPIWrapper, WikipediaAPIWrapper
from threading import Thread

from semantic_router import Route


class ToolResponse:
    def __init__(self, tool, text=None, error=None, link=None, image=None):
        self.tool = tool
        self.text = text
        self.error = error
        self.link = link
        self.image = image

class Tool:
    def __init__(self):
        self.ddg = DuckDuckGoSearchAPIWrapper()
        self.wolfram = WolframAlphaAPIWrapper()
        self.wikipedia = WikipediaAPIWrapper()
        self.schema = {
            'type': 'function',
            'function': {
                'name': 'web_search',
                'description': 'Search information about current events, famous people, etc on the internet.'
                               'Do NOT search weather forecast or time with it, you have separate functions for that',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'The search query or question for browser',
                        },
                    },
                    'required': ['query'],
                },
            },
        }
        self.route = Route(
            name='web_search',
            utterances=[
                'what is the semantic router',
                'what is the everest mountain',
                'what is compass',
                'what is '
                'who is',
                'how old is',
                'how long is',
                'and who is joe biden',
                "who is he",
                "who is his wife",
                "tell me about the war in ukraine",
                "who is trump",
                "what's the difference between",
                "who is",
                "what is oppenheimer movie about",
                "what is jku university",
                "who did",
                "is that true that",
                "what is his name?",
                "what is his age?",
                "how old is he?",
                "tell me about",
                "should i",
                "where is he from?",
                "tell me a joke",
                "is  alive",
                "how old is",
                "what is his name?",
                "what is his age?"])

    def run(self, query):
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