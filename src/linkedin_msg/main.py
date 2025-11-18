#!/usr/bin/env python
import sys
import os
import warnings
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
# override=True ensures we get the latest values even if already set
load_dotenv(override=True)

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.linkedin_msg.crew import LinkedinMsg


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew with inputs from environment variables.
    You can override these by editing the .env file.
    """
    print("====================================================================================")
    print("⚠️  DEPRECATION WARNING")
    print("====================================================================================")
    print("This synchronous script (main.py) is deprecated and will be removed in a future version.")
    print("Please use the asynchronous version for better performance, especially for batch processing.")
    print("\nTo run the async version for a single person:")
    print("python -m src.linkedin_msg.main_async")
    print("\nTo run in batch mode:")
    print("1. Set BATCH_MODE=true in your .env file.")
    print("2. Configure PERSON_NAMES and CONNECTION_NOTES in .env.")
    print("3. Run: python -m src.linkedin_msg.main_async")
    print("====================================================================================\n")

    # Load person name and connection note from environment variables
    # If not set, use default values
    person_name = os.getenv('PERSON_NAME', 'Harichandana Gonuguntla')
    connection_note = os.getenv('CONNECTION_NOTE',
        'Hi! I came across your profile and would love to connect. '
        'I\'m interested in your work and would like to expand my professional network. '
        'Looking forward to connecting with you!'
    )

    inputs = {
        'person_name': person_name,
        'connection_note': connection_note
    }

    try:
        LinkedinMsg().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        LinkedinMsg().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LinkedinMsg().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        LinkedinMsg().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    run()
