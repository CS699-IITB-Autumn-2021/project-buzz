import sqlite3
from dotenv import dotenv_values 
from flask import Flask,request,render_template
from flask_wtf.file import FileAllowed
from flask_wtf.form import FlaskForm 
import requests
from werkzeug.utils import redirect
from App import app
from datetime import datetime,timedelta


def fetchEnumTable(tableName,columns ):
	
	"""
	[This function extract data from database based on the tablename and columns given.]

    :parameter tablename , columns
	:return: [data/output of sqlite query]
	
	
	"""
	conn = sqlite3.connect('buzzDatabase.db',detect_types=sqlite3.PARSE_DECLTYPES |
							 sqlite3.PARSE_COLNAMES)
	cur = conn.cursor()
	query = "select "+columns+" from "+tableName
	data  = cur.execute(query).fetchall()
	return data

categoryList = fetchEnumTable("categories","id,name")
categoryDic = {val:key for key,val in categoryList}

@app.route('/viewProducts/<category>')
def viewProducts(category):
	"""
	[This function is used to render data to viewproducts page based on category]

	:param category: [string]
	:type : [string]
	:return: [final data of products]
	:rtype: [list]
	"""
	typeDic = {'any':" 1 ","fixed":" selling_option=1 ","bid":" selling_option=2 ","free":" selling_option=3 "}
	sortDic = {"date":" order by created_at DESC","priceHL":"order by price DESC ","priceLH":"order by price "}
	price = request.args.get('price') or 5000
	typeValue = request.args.get('type')  or 'any'
	typeValue = typeDic[typeValue]
	sort = request.args.get('sort') or "date"
	sortValue = sortDic[sort]
	price = int(price)

	if category=="all":
		data = fetchEnumTable("products where deleted_at is NULL and product_availability>0 and price <= %d  and bid_base<= %d and  %s %s"%(price,price,typeValue,sortValue),"title,price,product_availability,created_at,id,bid_base,bid_inc,selling_option")	
	else:
		data = fetchEnumTable("products where deleted_at is NULL and product_availability>0 and category_id=%d and price <= %d  and bid_base<= %d and  %s %s"%(categoryDic[category],price,price,typeValue,sortValue),"title,price,product_availability,created_at,id,bid_base,bid_inc,selling_option")	

	print(data)
	finalData =[]
	for element in data:
		pics=[]
		q = "images where product_id=\'%s\'  "%(element[4])
		pics = fetchEnumTable(q,"image_url")[0][0]	
		maxBid = fetchEnumTable("bid where product_id=\'%s\'"%(element[4]),"max(bid_price)")
		if maxBid[0][0] is None:
			maxBid="None"
		else:
			maxBid=maxBid[0][0]
		print(maxBid,"this is max bid")
		print(element[3],"==========\n",type(element[3]))
		temp = list(element)
		temp[3] = str(element[3])
		timeLeft = element[3]
		endTime = timeLeft + timedelta(hours = 24)
		finalTime=endTime - datetime.now()
		timeRemaining =""
		timeData = str(finalTime).split(":")
		if (int(timeData[0])>0):
			timeRemaining=str(timeData[0])+" hrs remaining"
		elif (int(timeData[1])>0):
			timeRemaining=str(timeData[1])+" mins remaining"
		else:
			timeRemaining="expired"
		print(endTime - datetime.now(),"THIS MUCH TIME LEFT")
		temp.append(pics)
		temp.append(maxBid)
		temp.append(str(timeRemaining))
		finalData.append(tuple(temp))
	print(finalData)
	print("type kya hai iska")
	print(type(finalData))

	return render_template('viewProducts.html',products=finalData)

# make the search bar input name as "query" in frontend
# reuse the viewProducts.html to display the search results by adding search.html
@app.route("/search", methods=['GET', 'POST'])
def search():
	"""
	[Make the search bar input name as "query" in frontend.
	Reuse the viewProducts.html to display the search results by adding search.html
	]

	:return: [It renders search.html with list of products]
	
	"""
	typeDic = {'any':" 1 ","fixed":" selling_option=1 ","bid":" selling_option=2 ","free":" selling_option=3 "}
	sortDic = {"date":" order by created_at DESC","priceHL":"order by price DESC ","priceLH":"order by price "}
	price = request.args.get('price') or 5000
	typeValue = request.args.get('type')  or 'any'
	typeValue = typeDic[typeValue]
	sort = request.args.get('sort') or "date"
	sortValue = sortDic[sort]
	price = int(price)
	query = request.args.get('query')
	# cur.execute("SELECT * FROM products")
	data = fetchEnumTable("products where deleted_at is NULL and product_availability>0 and price <= %d  and bid_base<= %d and  %s %s"%(price,price,typeValue,sortValue),"title,price,product_availability,created_at,id,bid_base,bid_inc,selling_option,product_description")	

	# records = fetchEnumTable("products","*")
	products = []
	for element in data:
		title = element[0].lower()
		description = element[8].lower()
		if title.find(query) == -1 and description.find(query) == -1:
			continue
		else:
			pics=[]
			q = "images where product_id=\'%s\'  "%(element[4])
			pics = fetchEnumTable(q,"image_url")[0][0]	
			maxBid = fetchEnumTable("bid where product_id=\'%s\'"%(element[4]),"max(bid_price)")
			if maxBid[0][0] is None:
				maxBid="None"
			else:
				maxBid=maxBid[0][0]
			print(maxBid,"this is max bid")
			print(element[3],"==========\n",type(element[3]))
			temp = list(element)
			temp[3] = str(element[3])
			timeLeft = element[3]
			endTime = timeLeft + timedelta(hours = 24)
			finalTime=endTime - datetime.now()
			timeRemaining =""
			timeData = str(finalTime).split(":")
			if (int(timeData[0])>0):
				timeRemaining=str(timeData[0])+" hrs remaining"
			elif (int(timeData[1])>0):
				timeRemaining=str(timeData[1])+" mins remaining"
			else:
				timeRemaining="expired"
			print(endTime - datetime.now(),"THIS MUCH TIME LEFT")
			temp.append(pics)
			temp.append(maxBid)
			temp.append(str(timeRemaining))
			products.append(tuple(temp))
			print(temp,"=======================\n")
			# products.append(rows)
	return render_template("search.html", products=products)
	# return render_template("viewProducts.html", products=products)
