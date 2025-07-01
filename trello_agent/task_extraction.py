import json
import re
from typing import List, Dict

from langchain_openai import ChatOpenAI
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

    print("🧪 Prompt:")
    print(prompt.format())
    print("🧪 Transcript:")
    print(transcript)

    response = chat.invoke([message, HumanMessage(content=transcript)])
    #print("🧪 Raw response from OpenAI:")
    #print(response.content)

    raw_content = response.content.strip()

    # Remove Markdown-style code block (```json ... ```)
    if raw_content.startswith("```") and raw_content.endswith("```"):
        raw_content = re.sub(r"^```[a-zA-Z]*\n", "", raw_content)
        raw_content = re.sub(r"\n```$", "", raw_content)

    try:
        tasks = json.loads(raw_content)
        if not isinstance(tasks, list):
            raise ValueError("Expected a list of tasks.")
    except Exception as e:
        print("⚠️ Failed to parse tasks:", e)
        tasks = []

    return tasks