import requests
import os

from todo_app.models.Item import Item

class TrelloClient():
    def __init__(self):
        self.key = os.getenv("TRELLO_KEY")
        self.token = os.getenv("TRELLO_TOKEN")
        self.board = os.getenv("TRELLO_BOARD_ID")

    def get_items(self):
        """
        Gets all items from the provided board id
        """
        payload = {
            'key': self.key,
            'token': self.token,
            'cards': 'open',
            'lists': 'open'
        }
        response = requests.get(f"https://api.trello.com/1/boards/{self.board}/", params=payload)
        data = response.json()
        cards = data["cards"]
        lists = data["lists"]

        items = []

        for card in cards:
            containing_list = [list for list in lists if list["id"] == card["idList"]]
            item = Item.from_trello_card(card, containing_list[0]["name"])
            items.append(item)
        
        return items

    def get_item(self, id):
        """
        Get an item for the provided id
            Args:
            id: The id of the item you are requesting
        """
        items = self.get_items()
        return next((item for item in items if item["id"] == id), None)
                
    def add_item(self, title):
        lists = self._get_lists()
        to_do_list = next((list for list in lists if list["name"] == "To-Do"), None)
        creation_params = {
            'key': self.key,
            'token': self.token,
            'name': title,
            'idList': to_do_list["id"]
        }
        requests.post("https://api.trello.com/1/cards", params=creation_params)

    def complete_item(self, id):
        lists = self._get_lists()
        complete_list = next((list for list in lists if list["name"] == "Completed"), None)
        payload = {
            'key': self.key,
            'token': self.token,
            'idList': complete_list["id"]
        }
        requests.put(f"https://api.trello.com/1/cards/{id}", payload)

    def delete_item(self, id):
        payload = {
            'key': self.key,
            'token': self.token, 
        }
        requests.delete(f"https://api.trello.com/1/cards/{id}", params=payload)

    def _get_lists(self):
        payload = {
            'key': self.key,
            'token': self.token,
            'lists': 'open'
        }
        response = requests.get(f"https://api.trello.com/1/boards/{self.board}/", params=payload)
        data = response.json()
        return data["lists"]

    def get_lists_by_id(self, id):
        lists = self._get_lists()
        return next((list for list in lists if list["id"] == id), None)

    
