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
	print("\n\n\n\n"+query)
	data  = cur.execute(query).fetchall()
	print(data)
	return data

@app.route('/')
def home():
	categoty = fetchEnumTable("categories","*")
	data = fetchEnumTable("products","title,bid_inc,product_availability,updated_at")	
	return render_template('buysell.html',products=data)

if __name__ == '__main__':
	app.run(debug=True)