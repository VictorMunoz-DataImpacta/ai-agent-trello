import os
from typing import Any, Dict, List

import requests

BASE_URL = "https://api.trello.com/1"


def _auth_params() -> Dict[str, str]:
    return {
        "key": os.environ["TRELLO_API_KEY"],
        "token": os.environ["TRELLO_TOKEN"],
    }


def get_cards(board_id: str) -> List[Dict[str, Any]]:
    url = f"{BASE_URL}/boards/{board_id}/cards"
    r = requests.get(url, params=_auth_params())
    r.raise_for_status()
    return r.json()


def create_card(list_id: str, name: str, desc: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/cards"
    params = {"idList": list_id, "name": name, "desc": desc, **_auth_params()}
    r = requests.post(url, params=params)
    r.raise_for_status()
    return r.json()


def update_card(card_id: str, name: str, desc: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/cards/{card_id}"
    params = {"name": name, "desc": desc, **_auth_params()}
    r = requests.put(url, params=params)
    r.raise_for_status()
    return r.json()
