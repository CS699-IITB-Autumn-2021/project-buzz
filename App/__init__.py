from flask import Flask
from dotenv import dotenv_values
import sqlite3
from flask_socketio import SocketIO


# configure app
app = Flask(__name__)
config = dotenv_values(".env")
app.secret_key = "super secret key"

# configuring the database
conn = sqlite3.connect('buzzDatabase.db',check_same_thread=False)
cur = conn.cursor()

# initialising socket-io
socketio = SocketIO(app)

from App import bingoClassifiedDbCode
from App import routes
from App import chat_event_buckets