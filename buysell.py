import sqlite3
from dotenv import dotenv_values 
from flask import Flask,request,render_template 
import requests
from werkzeug.utils import redirect
app = Flask(__name__)

def fetchEnumTable(tableName,columns ):
	conn = sqlite3.connect('buzzDatabase.db')
	cur = conn.cursor()
	query = "select "+columns+" from "+tableName
	data  = cur.execute(query).fetchall()
	print(data)
	return data

@app.route('/')
def home():

   return render_template('buysell.html')

if __name__ == '__main__':
	app.run(debug=True)