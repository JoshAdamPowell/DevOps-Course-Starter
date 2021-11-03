from flask import Flask, render_template, request, redirect
from .data.session_items import get_items, add_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template("index.html", items=items)

@app.route('/create', methods=["POST"])
def create_task():
    add_item(request.form.get('task_title'))
    return redirect('/')
