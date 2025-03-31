# -*- coding: utf-8 -*-
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
import asyncio
import os

# Load environment variables from .env file
load_dotenv()

async def main():
    # Initialize the LLM model
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,
    )
    
    # Configure the browser
    browser_config = BrowserConfig(
        headless=false,
        disable_security=True,
    )
    
    # Create browser instance
    browser = Browser(config=browser_config)
    
    # Create the agent with the model
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
        browser=browser,
        use_vision=true,
        save_conversation_path="logs/conversation",
    )
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Run the agent
    print(f"\nStarting Browser Use agent with task: Compare the price of gpt-4o and DeepSeek-V3")
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
