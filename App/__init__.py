import ssl
from flask import Flask
from dotenv import dotenv_values
import sqlite3
from flask_socketio import SocketIO
from pymongo import MongoClient


from flask_bootstrap import Bootstrap


# configure app
app = Flask(__name__)
Bootstrap(app)
config = dotenv_values(".env")
app.secret_key = "super secret key"

# configuring the database
conn = sqlite3.connect('buzzDatabase.db', check_same_thread=False)
cur = conn.cursor()

# initialising socket-io
socketio = SocketIO(app)

# configuring database for chat Application
client = MongoClient("mongodb+srv://test:test@project-buzz-chat-app.ovsu0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
chatDB = client.get_database("ChatDB")


from App import chatDBOperations
from App import routes
from App import viewProducts
from App import myAds
from App import addProducts
from App import chat_event_buckets
from App import profile

from App import chatDBOperations
from App import bingoClassifiedDbCode
from App import routes
from App import chat_event_buckets