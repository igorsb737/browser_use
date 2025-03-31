# Browser Use with AI Integration

This project demonstrates how to use the Browser Use library to create AI agents that can browse the web and perform tasks. The system integrates with LangChain chat models to provide a powerful web automation experience.

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install browser-use langchain-openai python-dotenv
   ```

2. **Install Playwright**:
   ```bash
   python -m playwright install
   ```

3. **Set up your API keys**:
   Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   # Add other API keys as needed (Anthropic, etc.)
   ```

## Demo Scripts

### 1. Basic OpenAI API Test (`openai_demo.py`)
A simple script to test your OpenAI API connection.

### 2. Basic Browser Use Demo (`browser_use_demo.py`)
A minimal example of using Browser Use with the OpenAI GPT-4o model.

### 3. Custom Browser Use Demo (`custom_browser_use_demo.py`)
A more comprehensive example with customizable settings:
- Custom system instructions
- Configurable headless mode
- Vision capabilities toggle
- Browser configuration options

## Usage Examples

### Basic Usage
```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

async def main():
    # Initialize the model
    llm = ChatOpenAI(model="gpt-4o")
    
    # Create agent with the model
    agent = Agent(
        task="Your task here",
        llm=llm
    )
    
    # Run the agent
    result = await agent.run()
    print(result)

asyncio.run(main())
```

### Advanced Usage with Custom Browser
```python
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio

# Configure the browser
browser = Browser(
    config=BrowserConfig(
        headless=False,
        disable_security=True,
        # Optional: Connect to your real Chrome browser
        # browser_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
)

# Create agent with custom settings
agent = Agent(
    task="Your task here",
    llm=ChatOpenAI(model="gpt-4o"),
    browser=browser,
    use_vision=True,
    save_conversation_path="logs/conversation",
    extend_system_message="Your custom instructions here"
)

async def main():
    result = await agent.run()
    print(result)
    await browser.close()

asyncio.run(main())
```

## Supported Models

Browser Use supports various LangChain chat models:

- **OpenAI**: GPT-4o (recommended for best performance)
- **DeepSeek**: DeepSeek-V3 (30 times cheaper than GPT-4o)
- **Gemini**: Gemini-2.0-exp (currently free)
- **Local models**: Like Qwen 2.5 (may have output structure issues)

## Customization Options

- **Browser Configuration**: Headless mode, security settings, proxy settings
- **System Prompt**: Extend or override the default system prompt
- **Vision Capabilities**: Enable/disable vision for better web interaction understanding
- **Real Browser Connection**: Connect to your existing Chrome browser with logged-in accounts

## Troubleshooting

- **Unicode Errors in Windows Command Prompt**: These are display issues and don't affect functionality
- **Browser Detection**: Some websites may detect headless browsers, try setting `headless=False`
- **API Key Issues**: Ensure your API keys are correctly set in the `.env` file

## Additional Resources

- [Browser Use Documentation](https://docs.browser-use.com/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
