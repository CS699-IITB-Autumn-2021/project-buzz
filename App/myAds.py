from datetime import datetime
import sqlite3
from dotenv import dotenv_values 
from flask import Flask,request,render_template, sessions 
from werkzeug.utils import redirect
from App import app
from flask import session
from App import conn, cur



def fetchEnumTable(tableName,columns ):
	"""
	[This function is used to fetch data from table given tablename and column name]

	:param tableName: [table from which data is to be fetched]
	:type tableName: [string]
	:param columns: [columns that need to be fetched]
	:type columns: [string]
	:return: [fetched data]
	
	"""
	conn = sqlite3.connect('buzzDatabase.db')
	cur = conn.cursor()
	query = "select "+columns+" from "+tableName
	print("\n\n\n\n"+query)
	data  = cur.execute(query).fetchall()
	print(data)
	return data

@app.route('/myAds')
def myAds():
	"""
	[If user is not logged in it will redirect user to home page else it will render myAds page where user can see all his/her ads.]

	
	"""
	userid = session.get('userId')
	if(userid == None):
		return redirect('/')
	print("I am session:",session)
	userId = session.get("userId")
	data = fetchEnumTable("products where user_id=\'%s\' and deleted_at is NULL"%(userId),"title,price,product_availability,updated_at,id,bid_base,bid_inc,selling_option,user_id")	
	print(data)
	finalData =[]
	for element in data:
		pics=[]
		q = "images where product_id=\'%s\' "%(element[4])
		pics = fetchEnumTable(q,"image_url")[0][0]	
		maxBid = fetchEnumTable("bid where product_id=\'%s\'"%(element[4]),"max(bid_price)")
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
	return render_template('myAds.html',products=finalData)


@app.route('/myAds/delete/<productId>')
def deleteMyAds(productId):
	"""
	[This function will delete ads with productid and will redirect to myAds page]

	
	"""
	
	userId = session.get("userId")
	q = """update products set deleted_at=\'%s\' where user_id=\'%s\' and id=\'%s\'"""%(datetime.now(),userId,productId)
	print(q)
	cur.execute(q)
	conn.commit()
	return redirect("/myAds")

@app.route('/myAds/sold/<productId>')
def sold(productId):
	"""
	[This function will mark ads with productid as sold and will redirect to myAds page]
    :parameter : productId
	
	
	"""
	
	userId = session.get("userId")
	q = """update products set product_availability=\'%d\' where user_id=\'%s\' and id=\'%s\'"""%(0,userId,productId)
	print(q)
	cur.execute(q)
	conn.commit()
	return redirect("/myAds")
