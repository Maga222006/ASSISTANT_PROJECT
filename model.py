import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class Generator:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv('OPENAI_API_BASE'),
            api_key=os.getenv('OPENAI_API_KEY')
        )

    def retrieve_messages(self):
        return [message for message in json.load(open('messages.json', 'r'))]

    def call_llm(self, messages, system_message, toolbox=None):
            response = self.client.chat.completions.create(
                model=os.getenv('TOOl_CALLING_MODEL' if toolbox else 'RESPONDING_MODEL'),
                messages=messages[:-1] + [system_message, messages[-1]],
                tools=toolbox
            ).choices[0]
            return response

