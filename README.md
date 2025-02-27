
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# AI Assistant Project

A powerful AI assistant project designed to help users with various tasks.

## Description

This project implements an AI-powered assistant capable of handling various user requests and tasks efficiently, with support for parallel task execution.

## Features

- AI-powered responses
- Task automation
- Natural language processing
- Interactive communication
- Multi-threaded task execution
- Parallel tool processing for improved performance
- Concurrent request handling

## API Endpoints

### POST /request
Send a request to the AI assistant:
```bash
curl -X POST "https://your-space-name.hf.space/request" \
     -H "Content-Type: application/json" \
     -d '{
       "messages": "[{\"role\": \"user\", \"content\": \"What's the weather like?\"}]",
       "openai_api_key": "your-api-key",
       "location": "London",
       "units": "metric"
     }'
```

## Getting Started

### Prerequisites

- Python 3.x
- Required dependencies (listed in requirements.txt)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Maga222006/ASSISTANT_PROJECT.git
```

2. Navigate to the project directory:
```bash
cd ASSISTANT_PROJECT
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The assistant supports parallel execution of tasks using multiple threads:

```python
# Example of parallel tool execution
assistant.run_tools_parallel([
    "tool1",
    "tool2",
    "tool3"
])
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Magomed Patakhov - [@Maga222006](https://github.com/Maga222006)

Project Link: [https://github.com/Maga222006/ASSISTANT_PROJECT](https://github.com/Maga222006/ASSISTANT_PROJECT) 
