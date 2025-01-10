import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import re
from openai.types.chat.chat_completion import Choice
from openai.types.chat import ChatCompletionMessageToolCall, ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import Function
load_dotenv()

class Generator:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv('OPENAI_API_BASE'),
            api_key=os.getenv('OPENAI_API_KEY')
        )

    def retrieve_messages(self):
        return [message for message in json.load(open('messages.json', 'r'))]

    def parse_tool_responses(self, content: str):
        function_regex = r"<function=(\w+)>\s*(\{.*?\})"
        matches = re.finditer(function_regex, content)
        result = Choice(
            finish_reason="function_call",
            index=0,
            message=ChatCompletionMessage(
                content=None,
                role='assistant',
                tool_calls=[]
            ),
        )
        for match in matches:
            name = match.group(1)
            arguments = match.group(2)
            result.message.tool_calls.append(
                ChatCompletionMessageToolCall(id='call', function=Function(name=name, arguments=arguments),
                                              type='function'))
        if result.message.tool_calls:
            return result
        else:
            return None

    def call_llm(self, messages, system_message, toolbox=None):
        response = self.client.chat.completions.create(
            model=os.getenv('TOOl_CALLING_MODEL' if toolbox else 'RESPONDING_MODEL'),
            messages=messages[:-1] + [system_message, messages[-1]],
            tools=toolbox
        ).choices[0]
        if toolbox and response.message.tool_calls or not toolbox:
            return response
        else:
            parsed_response=self.parse_tool_responses(response.message.content)
            if parsed_response:
                return parsed_response
            else:
                return response


