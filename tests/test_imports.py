import importlib
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

MODULES = [
    'trello_agent.task_extraction',
    'trello_agent.classifier',
    'trello_agent.trello_client',
]


def test_imports():
    for mod in MODULES:
        importlib.import_module(mod)
