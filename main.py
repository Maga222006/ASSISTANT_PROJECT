from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI
from tools import current_time
from dotenv import load_dotenv
from typing import Dict, Any
import json
import importlib
import threading
import logging
import os

load_dotenv()


class Agent:
    def __init__(self):
        self.llm = ChatOpenAI(model=os.getenv('MODEL'))
        self.current_time = current_time.Tool()
        self.uploaded_tools = self.load_tools()
        self.tools = [tool.schema for tool in self.uploaded_tools.values()]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

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
            'content': f"You are an AI assistant {os.getenv('ASSISTANT_NAME')}. "
                       f"The user is located in {os.getenv('LOCATION')}. "
                       f"If the user query requires real-time, up-to-date information, use tools, like 'web_search'. "
                       f"Use tools as often as possible. "
                       f"Make multiple simultaneous tool calls. "
        }
        response = self.llm_with_tools.invoke([system_message]+messages[-6:])

        def execute_tool(tool_name, command):
            try:
                arguments = json.loads(str(command)) if str(type(command)) != "<class 'dict'>" else command
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
        if response.tool_calls:
            calls = response.tool_calls
            threads = []
            if calls:
                for call in calls:
                    thread = threading.Thread(
                        target=execute_tool,
                        args=(call['name'], call['args'])
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
                    'content':
                        f"You are an AI assistant {os.getenv('ASSISTANT_NAME')}. "
                        f"The user is located in {os.getenv('LOCATION') or 'an unknown location'}. "
                        "You must answer the user **only** using the results from the tools. "
                        "Do not invent information that the tools did not provide. "
                        f"Tool Responses: "
                        f"{' '.join([f'*{tool_response.tool}: {tool_response.text if tool_response.text else tool_response.error},' for tool_response in tool_responses]) if tool_responses else 'None'}"
                }
                print(system_message)
                response = self.llm.invoke(messages[:-1]+[system_message, messages[-1]])
        agent_response['message'] = {'role': 'assistant', 'content': response.content}
        return agent_response


app = FastAPI()
agent = False


@app.post("/request")
async def process_request(request_body: Dict[str, Any]):
    global agent
    try:
        # Access fields from the raw dictionary
        messages = json.loads(request_body.get("messages", ""))
        os.environ['MODEL'] = request_body.get("model", "")
        os.environ['OPENAI_API_BASE'] = request_body.get("openai_api_base", "")
        os.environ['OPENAI_API_KEY'] = request_body.get("openai_api_key", "")
        os.environ['ASSISTANT_NAME'] = request_body.get("assistant_name", "")
        os.environ['LOCATION'] = request_body.get("location", "")
        os.environ['UNITS'] = request_body.get("units", "metric")
        if not agent:
            agent = Agent()
        response = agent.call_agent(messages)
        return response

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
