import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from browser_use import Agent, Browser, BrowserConfig

# Load environment variables
load_dotenv()

# DeepSeek API key
api_key = "sk-e0fe9106c3c14888b4322d8bf9f1b62f"

async def main():
    # Configure browser
    browser_config = BrowserConfig(
        headless=False,  # Set to True for headless mode
        disable_security=True,
        # Explicitly set window size to avoid 0 width issue
        extra_browser_args=["--window-size=1280,800"]
    )
    
    # Create browser instance
    browser = Browser(config=browser_config)
    
    # Initialize LLM with DeepSeek-R1
    llm = ChatOpenAI(
        base_url='https://api.deepseek.com/v1',
        model='deepseek-coder',  # Using deepseek-coder for R1
        api_key=api_key,
        temperature=0.0,
    )
    
    # Create agent
    agent = Agent(
        task="Go to https://www.google.com and search for 'deepseek ai models'",
        llm=llm,
        browser=browser,
        use_vision=False,  # Important: set to False for DeepSeek
        save_conversation_path="logs/conversation",
    )
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Run the agent
    print("\nStarting Browser Use agent with DeepSeek-R1...")
    result = await agent.run()
    
    # Print the result
    print("\n=== AGENT RESULT ===")
    print(result)
    print("===================")
    
    # Close the browser
    print("\nClosing browser...")
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
