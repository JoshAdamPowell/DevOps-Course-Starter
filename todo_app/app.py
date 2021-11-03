from flask import Flask, render_template, request, redirect
from .enums.task_status import Status
from .data.trello_items import get_items, add_item, complete_item, delete_item

app = Flask(__name__)

@app.route('/')
def index():
    items = get_items()
    completed_items = [item for item in items if item.status == Status.COMPLETED]
    incomplete_items = [item for item in items if item.status == Status.NOT_STARTED]
    return render_template("index.html", completed_items=completed_items, incomplete_items=incomplete_items)

@app.route('/create', methods=["POST"])
def create_task():
    add_item(request.form.get('task_title'))
    return redirect('/')

@app.route('/delete', methods=["POST"])
def delete_task():
    id = request.form.get("item_id")
    delete_item(id)
    return redirect("/")

@app.route('/complete', methods=["POST"])
def complete_task():
    id = request.form.get("item_id")
    complete_item(id)
    return redirect("/")
