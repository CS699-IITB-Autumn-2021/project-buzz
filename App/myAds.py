from datetime import datetime
import sqlite3
from dotenv import dotenv_values 
from flask import Flask,request,render_template, sessions 
from werkzeug.utils import redirect
from App import app
from flask import session
from App import conn, cur



def fetchEnumTable(tableName,columns ):
    conn = sqlite3.connect('buzzDatabase.db')
    cur = conn.cursor()
    query = "select "+columns+" from "+tableName
    print("\n\n\n\n"+query)
    data  = cur.execute(query).fetchall()
    print(data)
    return data

@app.route('/myAds')
def myAds():
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
    userId = session.get("userId")
    q = """update products set deleted_at=\'%s\' where user_id=\'%s\' and id=\'%s\'"""%(datetime.now(),userId,productId)
    print(q)
    cur.execute(q)
    conn.commit()
    # print("I am session:",session)
    # userId = session.get("userId")
    # data = fetchEnumTable("products where user_id=\'%s\' and deleted_at is NULL"%(userId),"title,price,product_availability,updated_at,id,bid_base,bid_inc,selling_option,user_id")	
    # print(data)
    # finalData =[]
    # for element in data:
    # 	pics=[]
    # 	q = "images where product_id=\'%s\' "%(element[4])
    # 	pics = fetchEnumTable(q,"image_url")[0][0]	
    # 	maxBid = fetchEnumTable("bid where product_id=\'%s\'"%(element[4]),"max(bid_price)")
    # 	if maxBid[0][0] is None:
    # 		maxBid="None"
    # 	else:
    # 		maxBid=maxBid[0][0]
    # 	print(maxBid,"this is max bid")
    # 	temp = list(element)
    # 	temp.append(pics)
    # 	temp.append(maxBid)
    # 	finalData.append(tuple(temp))
    # print(finalData)
    return redirect("/myAds")