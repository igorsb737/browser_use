import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

def test_openai_api():
    try:
        # Make a simple completion request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you today?"}
            ]
        )
        
        # Print the response
        print("API Response:")
        print(response.choices[0].message.content)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key.")
    else:
        print("Testing OpenAI API connection...")
        success = test_openai_api()
        if success:
            print("API test successful!")
        else:
            print("API test failed.")
