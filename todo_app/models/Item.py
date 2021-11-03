from todo_app.enums.task_status import Status


class Item:
    def __init__(self, id, name, status = Status.NOT_STARTED):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def get_status_for_list(cls, list_name):
        if (list_name == "To-Do"):
            return Status.NOT_STARTED
        return Status.COMPLETED

    @classmethod
    def from_trello_card(cls, card, list):
        status = Item.get_status_for_list(list)
        return cls(card['id'], card['name'], status)

