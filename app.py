from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
from pymongo import MongoClient, ReadPreference
from bson.objectid import ObjectId
# from bson.json_util import dumps

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

server = os.getenv("MONGO_SERVER")
port = int(os.getenv("MONGO_PORT"))
db_name = os.getenv("MONGO_DB_NAME")
col_name = os.getenv("MONGO_COL_NAME")

client = MongoClient(server, port,
    read_preference=ReadPreference.NEAREST)
db = client.get_database(db_name)

todos = db.todos

@app.route('/')
def index():
    saved_todos = todos.find()
    return render_template('index.html', todos=saved_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    todos.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

@app.route('/complete/<oid>')
def complete(oid):
    # Find _id
    filter = { '_id': ObjectId(oid) }
    # Values to be updated.
    newvalues = { "$set": { 'complete': True } }
    todos.update_one(filter, newvalues)
    return redirect(url_for('index'))


@app.route('/delete_completed')
def delete_completed():
    todos.delete_many({'complete' : True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    todos.delete_many({})
    return redirect(url_for('index'))

if (__name__) == "__main__":
    app.run(debug=True)