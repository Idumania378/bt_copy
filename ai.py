import os
from openai import OpenAI, APIStatusError, APIConnectionError, RateLimitError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Key and Client Initialization ---
# Get the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# IMPORTANT: This print statement must come AFTER api_key is defined
# For security, only show the last few characters of the API key
print(f"API Key Loaded (last 4 chars): {api_key[-4:] if api_key else 'None'}")
if not api_key:
    print("CRITICAL ERROR: OPENAI_API_KEY is not set in your .env file or environment variables.")
    # In a production app, you might want to raise an exception or exit here.

# Initialize the OpenAI client
try:
    client = OpenAI(
        api_key=api_key
    )
    # Optional: You can add a small test call here to confirm connectivity, e.g.:
    # client.models.list()
    # print("OpenAI client initialized successfully.")
except Exception as e:
    print(f"Error initializing OpenAI client. Make sure OPENAI_API_KEY is correct: {e}")
    # Consider raising an error here or setting a flag to prevent further API calls.

# Define the default model to use for general responses
# "gpt-4o" is currently OpenAI's most capable and efficient model.
# "gpt-3.5-turbo" is a good, more cost-effective option for simpler tasks.
DEFAULT_RESPONSE_MODEL = "gpt-4o"
DEFAULT_DETECTION_MODEL = "gpt-3.5-turbo" # More cost-effective for simple classification

def openai_chat_completion(messages, model=DEFAULT_RESPONSE_MODEL, temperature=0.7, max_tokens=1000):
    """
    Makes a chat completion request to the OpenAI API.

    Args:
        messages (list): A list of message dictionaries for the conversation.
        model (str): The name of the OpenAI model to use.
        temperature (float): Controls randomness of the output (0.0 to 2.0).
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        str: The content of the AI's response.

    Raises:
        APIStatusError: For HTTP errors (e.g., 400, 401, 429, 500).
        APIConnectionError: For network-related errors.
        RateLimitError: If you exceed OpenAI's rate limits.
        Exception: For other unexpected errors.
    """
    try:
        # Debugging: Print messages being sent to the API
        print(f"\n--- OpenAI API Request ---")
        print(f"Model: {model}")
        print(f"Messages: {messages}")
        print(f"Temperature: {temperature}, Max Tokens: {max_tokens}")
        print(f"--- End Request ---")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        response_content = response.choices[0].message.content.strip()
        print(f"\n--- OpenAI API Response ---")
        print(f"Response content: {response_content}")
        print(f"--- End Response ---")
        return response_content
    except APIStatusError as e:
        print(f"ERROR: OpenAI API Status Error (Status {e.status_code}): {e.response}")
        raise # Re-raise for Streamlit to display
    except APIConnectionError as e:
        print(f"ERROR: OpenAI Connection Error: Could not connect to API. {e}")
        raise # Re-raise
    except RateLimitError as e:
        print(f"ERROR: OpenAI Rate Limit Error: {e}")
        raise # Re-raise
    except Exception as e:
        print(f"ERROR: An unexpected error occurred during OpenAI API call: {e}")
        raise # Re-raise


def detect_subject(question):
    """
    Detects the subject of a homework question using the OpenAI API.
    """
    try:
        messages = [
            {"role": "system", "content": "You are a subject detection assistant. Analyze the following homework question and respond with ONLY the subject it belongs to. Possible subjects: Math, English, Science, Kiswahili, Social Studies, CRE, or Other."},
            {"role": "user", "content": question}
        ]
        # Use a more deterministic and cost-effective model for classification
        return openai_chat_completion(messages, model=DEFAULT_DETECTION_MODEL, temperature=0.1, max_tokens=10)
    except Exception as e:
        print("Error detecting subject:", e)
        return "Other"


def generate_response(question, subject, step_by_step=False, simple_explanation=False):
    """
    Generates a homework explanation using the OpenAI API.
    """
    try:
        system_prompt = f"""
        You are a helpful homework assistant for Kenyan parents helping their children with CBC curriculum (Grades 4-9).
        The subject is {subject}.
        Provide a clear, concise explanation that a parent can use to explain to their child.
        """
        if simple_explanation:
            system_prompt += " Explain this to a 10-year-old using simple language and relatable examples from Kenya."
        if step_by_step:
            system_prompt += " Break down the solution into clear, numbered steps."
        system_prompt += " Use friendly, encouraging language. If it's a math problem, explain the concepts before solving."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        return openai_chat_completion(messages, model=DEFAULT_RESPONSE_MODEL)
    except Exception as e:
        print("Error generating response:", e)
        return "Sorry, I couldn't generate a response. Please try again later."