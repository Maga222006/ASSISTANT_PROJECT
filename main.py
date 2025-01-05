import datetime
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from model import Generator
import json
import importlib
import threading
import logging
load_dotenv()


class Agent:
    def __init__(self):
        self.generator = Generator()
        self.uploaded_tools = self.load_tools()
        self.toolbox = [tool.schema for tool in self.uploaded_tools.values()]

    def load_tools(self):
        """Dynamically load skill modules from the 'tools' directory."""
        skills = {}
        for root, _, files in os.walk('tools'):
            for file_name in files:
                if file_name.endswith('.py'):
                    module_name = os.path.splitext(file_name)[0]
                    try:
                        tool_module = importlib.import_module(f'tools.{module_name}')
                        tool_instance = getattr(tool_module, 'Tool')()
                        skills[module_name] = tool_instance
                    except (ImportError, AttributeError) as e:
                        logging.error(f"Error loading skill '{module_name}': {e}")
        return skills

    def call_agent(self, messages):
        agent_response = {
            "status": "success",
            "message": None,
            "links": [],
            "location": None,
            "alarm": None,
            "timer": None,
            "stopwatch": None
        }
        tool_responses = []
        system_message = {
            'role': 'system',
            'content': (
                f"You are helpful AI assistant {f'''named {os.getenv('ASSISTANT_NAME')}.''' if os.getenv('ASSISTANT_NAME') else '''.'''}"
                f'Your job is to give the response to the user query using tools.'
                f'EVERY TIME you need up-to-date information (weather forecast, current time, famous people, web search), call the tools.'
                f"Tools available: {(tool['function']['name'] for tool in self.toolbox)}"
                f'Call tools AS OFTEN AS YOU CAN.'
                f'You can make MULTIPLE PARALLEL parallel tool calls.'
            )
        }
        response = self.generator.call_llm(messages=messages, toolbox=self.toolbox, system_message=system_message)

        def execute_tool(tool_name, command):
            try:
                arguments = json.loads(str(command))
                if arguments:
                    tool_response = self.uploaded_tools[tool_name].run(**arguments)
                else:
                    tool_response = self.uploaded_tools[tool_name].run()
                if tool_response:
                    tool_responses.append(tool_response)

            except:
                tool_response = self.uploaded_tools[tool_name].run()
                if tool_response:
                    tool_responses.append(tool_response)

        # Step 3: If the LLM used any tools, run them
        if response.message.tool_calls:

            calls = response.message.tool_calls
            threads = []
            if calls:
                for call in calls:
                    thread = threading.Thread(
                        target=execute_tool,
                        args=(call.function.name, call.function.arguments)
                    )
                    thread.start()
                    threads.append(thread)

                for thread in threads:
                    thread.join()

                for tool_response in tool_responses:
                    if tool_response.stopwatch: agent_response["stopwatch"] = tool_response.stopwatch
                    if tool_response.location: agent_response["location"] = tool_response.location
                    if tool_response.link: agent_response["links"].append(tool_response.link)
                    if tool_response.timer: agent_response["timer"] = tool_response.timer
                    if tool_response.alarm: agent_response["alarm"] = tool_response.alarm

                system_message = {
                    'role': 'system',
                    'content': (
                        f"You are a helpful AI assistant {os.getenv('ASSISTANT_NAME')}"
                        f"Your primary responsibility is to respond to user queries strictly based on the tool responses provided below. "
                        f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}. "
                        f"Tool Responses: {', '.join([f'{tool_response.tool}: {tool_response.text if tool_response.text else tool_response.error}' for tool_response in tool_responses]) if tool_responses else 'None available'}."
                    )
                }
                response =  self.generator.call_llm(messages=messages, system_message=system_message)
        agent_response['message'] = {'role': 'assistant', 'content': response.message.content}
        return agent_response

app = FastAPI()
agent = False

@app.post("/request")
async def process_request(request_body: Dict[str, Any]):
    global agent
    try:
        # Access fields from the raw dictionary
        messages = json.loads(request_body.get("messages", ""))
        os.environ['OPENWEATHERMAP_API_KEY'] = request_body.get("openweathermap_api_key", "50b35515160c2d0256e022dae872895b")
        os.environ['WOLFRAM_ALPHA_APPID'] = request_body.get("wolfram_alpha_appid", "AVQW9H-UX8U8TU5KU")
        os.environ['TOOl_CALLING_MODEL'] = request_body.get("tool_calling_model", "")
        os.environ['RESPONDING_MODEL'] = request_body.get("responding_model", "")
        os.environ['OPENAI_API_BASE'] = request_body.get("openai_api_base", "")
        os.environ['OPENAI_API_KEY'] = request_body.get("openai_api_key", "")
        os.environ['ASSISTANT_NAME'] = request_body.get("assistant_name", "")
        os.environ['LOCATION'] = request_body.get("location", "")
        os.environ['UNITS'] = request_body.get("units", "metric")
        if not agent:
            agent = Agent()
        response = agent.call_agent(messages)
        print(response)
        return response

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
