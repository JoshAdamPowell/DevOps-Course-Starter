from flask import Flask, render_template, request, redirect
from .enums.task_status import Status
from .data.trello_items import TrelloClient

app = Flask(__name__)
trello_client = TrelloClient()

@app.route('/')
def index():
    items = trello_client.get_items()
    completed_items = [item for item in items if item.status == Status.COMPLETED]
    incomplete_items = [item for item in items if item.status == Status.NOT_STARTED]
    return render_template("index.html", completed_items=completed_items, incomplete_items=incomplete_items)

@app.route('/create', methods=["POST"])
def create_task():
    trello_client.add_item(request.form.get('task_title'))
    return redirect('/')

@app.route('/delete', methods=["POST"])
def delete_task():
    id = request.form.get("item_id")
    trello_client.delete_item(id)
    return redirect("/")

@app.route('/complete', methods=["POST"])
def complete_task():
    id = request.form.get("item_id")
    trello_client.complete_item(id)
    return redirect("/")
