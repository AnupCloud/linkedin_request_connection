#!/usr/bin/env python
"""
Async version of LinkedIn automation for batch processing multiple people.
This allows sending connection requests to multiple people in parallel.
"""

import sys
import os
import warnings
import asyncio
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv(override=True)

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.linkedin_msg.crew import LinkedinMsg

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


async def run_single(person_name: str, connection_note: str):
    """
    Run automation for a single person asynchronously.
    """
    print(f"\n🚀 Starting automation for: {person_name}")

    inputs = {
        'person_name': person_name,
        'connection_note': connection_note
    }

    try:
        # Use async kickoff
        result = await LinkedinMsg().crew().kickoff_async(inputs=inputs)
        print(f"✅ Completed for: {person_name}")
        return {'person': person_name, 'status': 'success', 'result': result}
    except Exception as e:
        print(f"❌ Failed for {person_name}: {str(e)}")
        return {'person': person_name, 'status': 'failed', 'error': str(e)}


async def run_batch(people: list):
    """
    Run automation for multiple people in parallel.

    Args:
        people: List of dicts with 'name' and 'note' keys

    Example:
        people = [
            {'name': 'John Smith', 'note': 'Hi John! ...'},
            {'name': 'Jane Doe', 'note': 'Hi Jane! ...'},
            {'name': 'Bob Wilson', 'note': 'Hi Bob! ...'}
        ]
    """
    print(f"\n{'='*60}")
    print(f"🔗 LinkedIn Batch Automation")
    print(f"{'='*60}")
    print(f"📊 Processing {len(people)} connection requests in parallel")
    print(f"{'='*60}\n")

    # Create tasks for all people
    tasks = [
        run_single(person['name'], person['note'])
        for person in people
    ]

    # Run all tasks in parallel
    start_time = datetime.now()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = datetime.now()

    # Print summary
    elapsed_time = (end_time - start_time).total_seconds()
    successful = sum(1 for r in results if isinstance(r, dict) and r.get('status') == 'success')
    failed = len(results) - successful

    print(f"\n{'='*60}")
    print(f"📊 BATCH AUTOMATION SUMMARY")
    print(f"{'='*60}")
    print(f"⏱️  Total Time: {elapsed_time:.1f} seconds")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Average Time per Person: {elapsed_time/len(people):.1f} seconds")
    print(f"{'='*60}\n")

    return results


async def run():
    """
    Single person automation (asynchronous).
    """
    person_name = os.getenv('PERSON_NAME', 'John Smith')
    connection_note = os.getenv('CONNECTION_NOTE',
        'Hi! I came across your profile and would love to connect.')

    inputs = {
        'person_name': person_name,
        'connection_note': connection_note
    }

    try:
        # Use async kickoff for single run
        result = await LinkedinMsg().crew().kickoff_async(inputs=inputs)
        print("\n\n########################")
        print("## Here is the result")
        print("########################\n")
        print(result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def run_batch_sync():
    """
    Batch automation - runs async tasks from sync context.

    Usage:
        Set environment variable BATCH_MODE=true and provide
        PERSON_NAMES and CONNECTION_NOTES as comma-separated values.
    """
    # Check if batch mode
    batch_mode = os.getenv('BATCH_MODE', 'false').lower() == 'true'

    if not batch_mode:
        print("❌ BATCH_MODE not enabled. Set BATCH_MODE=true in .env")
        return

    # Parse comma-separated names and notes
    names = os.getenv('PERSON_NAMES', '').split(',')
    notes = os.getenv('CONNECTION_NOTES', '').split('|')

    # Clean up whitespace
    names = [name.strip() for name in names if name.strip()]
    notes = [note.strip() for note in notes if note.strip()]

    if not names:
        print("❌ No names provided. Set PERSON_NAMES in .env (comma-separated)")
        return

    # If only one note provided, use it for all
    if len(notes) == 1:
        notes = notes * len(names)
    elif len(notes) != len(names):
        print(f"⚠️  Warning: {len(names)} names but {len(notes)} notes. Using first note for all.")
        notes = [notes[0] if notes else "Hi! Would love to connect."] * len(names)

    # Create people list
    people = [
        {'name': name, 'note': note}
        for name, note in zip(names, notes)
    ]

    # Run async batch
    asyncio.run(run_batch(people))


if __name__ == "__main__":
    # Check if batch mode
    if os.getenv('BATCH_MODE', 'false').lower() == 'true':
        run_batch_sync()
    else:
        asyncio.run(run())
