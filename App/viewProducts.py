import sqlite3
from dotenv import dotenv_values 
from flask import Flask,request,render_template 
import requests
from werkzeug.utils import redirect
from App import app

def fetchEnumTable(tableName,columns ):
	conn = sqlite3.connect('buzzDatabase.db')
	cur = conn.cursor()
	query = "select "+columns+" from "+tableName
	print("\n\n\n\n"+query)
	data  = cur.execute(query).fetchall()
	print(data)
	return data

@app.route('/viewProducts')
def viewProducts():
	categoty = fetchEnumTable("categories","*")
	data = fetchEnumTable("products","title,price,product_availability,updated_at,id,bid_base,bid_inc,selling_option")	
	print(data)
	finalData =[]
	for element in data:
		print("I am element ",element)
		pics=[]
		q = "images where product_id=\'%s\'"%(element[4])
		pics = fetchEnumTable(q,"image_url")[0][0]	
		maxBid = fetchEnumTable("bid where product_id=\'%s\'"%(element[4]),"max(bid_price)")
		print("======\t",pics,maxBid)
		if maxBid[0][0] is None:
			maxBid="None"
		else:
			maxBid=maxBid[0][0]
		print(maxBid,"this is max bid")
		temp = list(element)
		temp.append(pics)
		temp.append(maxBid)
		finalData.append(tuple(temp))
	print(finalData)

	return render_template('viewProducts.html',products=finalData)
