import requests
import os

from todo_app.models.Item import Item
from ..enums.task_status import Status

def get_items():
    """
    Gets all items from the provided board id
    """
    key = os.getenv("TRELLO_KEY")
    token = os.getenv("TRELLO_TOKEN")
    board = os.getenv("TRELLO_BOARD_ID")
    payload = {
        'key': key,
        'token': token,
        'cards': 'open',
        'lists': 'open'
    }
    response = requests.get(f"https://api.trello.com/1/boards/{board}/", params=payload)
    data = response.json()
    cards = data["cards"]
    lists = data["lists"]

    items = []

    for card in cards:
        containing_list = [list for list in lists if list["id"] == card["idList"]]
        item = Item.from_trello_card(card, containing_list[0]["name"])
        items.append(item)
    
    return items

def get_item(id):
    """
    Get an item for the provided id
        Args:
        id: The id of the item you are requesting
    """
    items = get_items
    return next((item for item in items if item["id"] == id), None)
            
def add_item(title):
    key = os.getenv("TRELLO_KEY")
    token = os.getenv("TRELLO_TOKEN")
    lists = _get_lists()
    to_do_list = next((list for list in lists if list["name"] == "To-Do"), None)
    creation_params = {
        'key': key,
        'token': token,
        'name': title,
        'idList': to_do_list["id"]
    }
    requests.post("https://api.trello.com/1/cards", params=creation_params)

def complete_item(id):
    key = os.getenv("TRELLO_KEY")
    token = os.getenv("TRELLO_TOKEN")
    lists = _get_lists()
    complete_list = next((list for list in lists if list["name"] == "Completed"), None)
    payload = {
        'key': key,
        'token': token,
        'idList': complete_list["id"]
    }
    requests.put(f"https://api.trello.com/1/cards/{id}", payload)

def delete_item(id):
    key = os.getenv("TRELLO_KEY")
    token = os.getenv("TRELLO_TOKEN")   
    payload = {
        'key': key,
        'token': token, 
    }
    requests.delete(f"https://api.trello.com/1/cards/{id}", params=payload)

def _get_lists():
    key = os.getenv("TRELLO_KEY")
    token = os.getenv("TRELLO_TOKEN")
    board = os.getenv("TRELLO_BOARD_ID")
    payload = {
        'key': key,
        'token': token,
        'lists': 'open'
    }
    response = requests.get(f"https://api.trello.com/1/boards/{board}/", params=payload)
    data = response.json()
    return data["lists"]
