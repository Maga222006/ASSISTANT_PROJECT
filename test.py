import requests
import json

# The URL of your API
API_URL = "http://0.0.0.0:8000/request"  # Update this with your actual HF space URL

# Test message
messages = [
    {"role": "user", "content": "What's the weather like today?"}
]

# Prepare the request body
request_body = {
    "messages": json.dumps(messages),
    "openai_api_key": "your-openai-api-key",  # Replace with your OpenAI API key
    "location": "London",  # Example location
    "units": "metric"
}

try:
    # Send POST request to the API
    response = requests.post(API_URL, json=request_body)
    
    # Check if request was successful
    if response.status_code == 200:
        print("Success! Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: Status code {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Error occurred: {str(e)}") 