import os
from typing import List, Dict

import streamlit as st
from dotenv import load_dotenv

from trello_agent.task_extraction import extract_tasks
from trello_agent.classifier import ProjectClassifier
from trello_agent.trello_client import create_card, get_cards


def load_env() -> None:
    if os.path.exists('.env'):
        load_dotenv('.env')


def main() -> None:
    load_env()
    st.title('AI Trello Agent')
    transcript_file = st.file_uploader('Upload transcript', type=['txt'])
    if transcript_file:
        transcript = transcript_file.read().decode('utf-8')
        tasks = extract_tasks(transcript, os.environ['OPENAI_API_KEY'])
        if tasks:
            st.subheader('Extracted Tasks')
            for i, task in enumerate(tasks, 1):
                st.text(f"{i}. {task['description']}")
        else:
            st.write('No tasks found')

        if st.button('Sync to Trello'):
            board_id = os.environ.get('TRELLO_BOARD_ID')
            cards = get_cards(board_id)
            for task in tasks:
                create_card(board_id, task['description'], '')
            st.success('Synced to Trello!')


if __name__ == '__main__':
    main()
