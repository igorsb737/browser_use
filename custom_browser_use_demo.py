from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig
from dotenv import load_dotenv
import asyncio
import os

# Load environment variables from .env file
load_dotenv()

# Custom system prompt extension to modify agent behavior
CUSTOM_INSTRUCTIONS = """
ADDITIONAL INSTRUCTIONS:
1. When searching for information, always try to find the most recent data available.
2. Summarize information in a clear, concise manner.
3. If you encounter any paywalls or login pages, try to find alternative sources.
"""

async def run_browser_use_agent(task, headless=False, use_vision=True, custom_instructions=None):
    """
    Run a Browser Use agent with customizable settings
    
    Args:
        task (str): The task for the agent to perform
        headless (bool): Whether to run the browser in headless mode
        use_vision (bool): Whether to enable vision capabilities
        custom_instructions (str): Custom instructions to extend the system prompt
    
    Returns:
        str: The result of the agent's execution
    """
    # Initialize the LLM model
    llm = ChatOpenAI(
        model="gpt-4o",  # You can change this to other models like "gpt-3.5-turbo" for lower cost
        temperature=0.0,
    )
    
    # Configure the browser
    browser_config = BrowserConfig(
        headless=headless,
        disable_security=True,
        # You can uncomment the line below to use your own Chrome browser
        # browser_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
    
    # Create browser instance
    browser = Browser(config=browser_config)
    
    # Create the agent with the model
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        use_vision=use_vision,
        save_conversation_path="logs/conversation",
        extend_system_message=custom_instructions
    )
    
    # Run the agent
    print(f"\nStarting Browser Use agent with task: {task}")
    result = await agent.run()
    
    # Close the browser
    print("\nClosing browser...")
    await browser.close()
    
    return result

async def main():
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Define a task for the agent
    task = "Compare the pricing and features of GPT-4o and DeepSeek-V3 models. Create a brief summary of the differences."
    
    # Run the agent with custom instructions
    result = await run_browser_use_agent(
        task=task,
        headless=False,  # Set to True to hide the browser window
        use_vision=True,  # Enable vision capabilities
        custom_instructions=CUSTOM_INSTRUCTIONS
    )
    
    # Print the result
    print("\n=== AGENT RESULT ===")
    print(result)
    print("===================")

if __name__ == "__main__":
    asyncio.run(main())
