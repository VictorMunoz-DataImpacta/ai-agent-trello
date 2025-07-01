import os

import streamlit as st
from dotenv import load_dotenv

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from trello_agent.task_extraction import extract_tasks
from trello_agent.trello_client import (
    find_duplicates,
    sync_tasks,
)


def load_env() -> None:
    if os.path.exists('.env'):
        load_dotenv('.env')


def handle_user_message(message: str) -> str:
    """Respond to user queries and optionally interact with Trello."""
    board_id = os.environ.get('TRELLO_BOARD_ID')
    if message.lower().startswith('review trello') or 'duplicate' in message.lower():
        dups = find_duplicates(board_id, st.session_state.get('tasks', []))
        if dups:
            return 'This are the Duplicates:\n' + '\n'.join(f'- {d}' for d in dups)
        return 'No duplicates found.'
    if message.lower().startswith('sync') or 'upload' in message.lower():
        sync_tasks(board_id, st.session_state.get('tasks', []))
        return 'Synced tasks to Trello.'

    chat = ChatOpenAI(openai_api_key=os.environ['OPENAI_API_KEY'], temperature=0)
    history = [
        HumanMessage(m['content']) if m['role'] == 'user' else AIMessage(m['content'])
        for m in st.session_state.get('messages', [])
    ]
    history.append(HumanMessage(message))
    resp = chat.invoke([SystemMessage('You are a helpful assistant for task management.')]+history)
    return resp.content


def main() -> None:
    load_env()
    st.title('AI Trello Agent')

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    transcript_file = st.file_uploader('Upload transcript', type=['txt'])
    if transcript_file:
        transcript = transcript_file.read().decode('utf-8')
        st.session_state.tasks = extract_tasks(transcript, os.environ['OPENAI_API_KEY'])
        if st.session_state.tasks:
            st.subheader('Extracted Tasks')
            for i, task in enumerate(st.session_state.tasks, 1):
                st.text(f"{i}. {task['description']}")
        else:
            st.write('No tasks found')

        if st.button('Sync to Trello'):
            board_id = os.environ.get('TRELLO_BOARD_ID')
            sync_tasks(board_id, st.session_state.tasks)
            st.success('Synced to Trello!')

    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])

    prompt = st.chat_input('Ask a question')
    if prompt:
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        response = handle_user_message(prompt)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.chat_message('assistant').write(response)


if __name__ == '__main__':
    main()
