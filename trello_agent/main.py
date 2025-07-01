# pylint: disable=import-error

import os
from typing import List, Dict

from dotenv import load_dotenv

from .task_extraction import extract_tasks
from .classifier import ProjectClassifier
from .trello_client import create_card, get_cards


def load_env() -> None:
    if os.path.exists('.env'):
        load_dotenv('.env')


def process_transcript(transcript: str) -> List[Dict[str, str]]:
    openai_key = os.environ['OPENAI_API_KEY']
    tasks = extract_tasks(transcript, openai_key)
    return tasks


if __name__ == '__main__':
    import sys

    load_env()
    if len(sys.argv) < 2:
        print('Usage: python -m trello_agent.main <transcript.txt>')
        raise SystemExit(1)

    with open(sys.argv[1], 'r') as f:
        transcript = f.read()

    tasks = process_transcript(transcript)
    print(tasks)
