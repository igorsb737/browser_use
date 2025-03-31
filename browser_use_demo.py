from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

async def main():
    # Initialize the LLM model (GPT-4o for best performance)
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,
    )
    
    # Configure the browser
    browser = Browser(
        config=BrowserConfig(
            headless=False,  # Set to True if you don't want to see the browser
            disable_security=True
        )
    )
    
    # Create the agent with the model
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",  # Example task
        llm=llm,
        browser=browser,
        use_vision=True,  # Enable vision capabilities
        save_conversation_path="logs/conversation"  # Save chat logs
    )
    
    # Run the agent
    print("Starting Browser Use agent...")
    result = await agent.run()
    
    # Print the result
    print("\nAgent Result:")
    print(result)
    
    # Close the browser
    print("\nClosing browser...")
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
