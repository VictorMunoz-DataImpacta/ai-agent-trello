import json
from typing import List, Dict

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage


PROMPT_TEMPLATE = (
    "You will be given a meeting transcript. "
    "Extract all actionable tasks and output them as a JSON array. "
    "Each task should have a 'description' field."
)


def extract_tasks(transcript: str, openai_api_key: str) -> List[Dict[str, str]]:
    """Use an LLM to extract tasks from a transcript."""
    chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    message = HumanMessage(content=prompt.format())
    response = chat([message, HumanMessage(content=transcript)])
    try:
        tasks = json.loads(response.content)
        assert isinstance(tasks, list)
    except Exception:
        tasks = []
    return tasks
