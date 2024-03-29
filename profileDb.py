

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email


import sqlite3

conn = sqlite3.connect('buzzDatabase.db')
cur = conn.cursor()
with open('SqlFile.sql') as f:
    conn.executescript(f.read())
    


cur.execute("""INSERT INTO sex(name) VALUES("male") """)
cur.execute("""INSERT INTO sex(name) VALUES("female") """)
cur.execute("""INSERT INTO sex(name) VALUES("others") """)
cur.execute("SELECT * FROM sex")
records = cur.fetchall()

cur.execute("""INSERT INTO user VALUES("1","Deeksha","Kasture","abc@iitb.ac.in",9876543210,2,213050072,1,NULL,NULL,NULL) """)
cur.execute("""SELECT  first_name,last_name,sex.name,email,contact_no FROM user,sex  WHERE user_id='1' and user.sex_id = sex.id """)


record = cur.fetchall()
for data in record:
    print(data)

fname = record[0][0]
print(type(record))
lname = record[0][1]
name = fname+" "+lname
sex = record[0][2]
email = record[0][3]
contact = record[0][4]
print(name)
print(sex)
print(email)
print(contact)
cur.execute("""Insert into products values(NULL,2,"1","A good book in good condition",500,"BOOK",2,100,4,0,1,1,20,NULL,NULL,NULL) """)
cur.execute("""Select * from products , user where products.user_id = user.user_id and products.id=1 """)
details = cur.fetchall()
description = details[0][3]
price = details[0][4]
title=details[0][5]
likes = details[0][7]
dislikes =details[0][8]
contact_no = details[0][20]
postedon = details[0][13]
seller = details[0][5]








conn.close()



class NameForm(FlaskForm):
    # email = StringField('Email ID ', [validators.Email(message="invalid email")])
    email = EmailField("Email ",  [InputRequired("Please enter your email address.")])

    submit = SubmitField('Submit')






app = Flask(__name__)
Bootstrap(app)

# # # Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

@app.route('/detail', methods=['GET', 'POST'])
def detail():
    

    
    return render_template('detail.html',description =description,price =price,title=title,likes=likes,dislikes=dislikes ,contact_no=contact_no ,postedon=postedon ,seller=seller
)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        newemail = form.newemail.data
        print(newemail)

    
    return render_template('profile.html',name=name,sex=sex,email=email,contact=contact,form=form)

if __name__ == '__main__':
	app.run(host="127.0.30.45",port="5023",debug=True)




