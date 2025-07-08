# test_ai.py
import os
from dotenv import load_dotenv

# Load environment variables (important for this test script too)
load_dotenv()

# Import your AI functions
from ai import generate_response, detect_subject

print("--- Testing Subject Detection ---")
question_to_test = "What is the formula for calculating speed?"
subject = detect_subject(question_to_test)
print(f"Question: '{question_to_test}'")
print(f"Detected Subject: {subject}")

print("\n--- Testing Response Generation ---")
response = generate_response(question_to_test, subject, step_by_step=True, simple_explanation=False)
print(f"Generated Response:\n{response}")

print("\n--- Test Complete ---")