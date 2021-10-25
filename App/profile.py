import sqlite3
from App import app
from flask import session
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email

conn = sqlite3.connect('buzzDatabase.db')
cur = conn.cursor()
with open('SqlFile.sql') as f:
    conn.executescript(f.read())

# userId = session.get('userId')



# cur.execute("""INSERT INTO user VALUES("1","Deeksha","Kasture","abc@iitb.ac.in",9876543210,2,213050072,1,NULL,NULL,NULL) """)
# cur.execute("""SELECT  first_name,last_name,sex.name,email,contact_no FROM user,sex  WHERE user_id=userId and user.sex_id = sex.id """)


# record = cur.fetchall()
# for data in record:
#     print(data)

# fname = record[0][0]
# print(type(record))
# lname = record[0][1]
# name = fname+" "+lname
# sex = record[0][2]
# email = record[0][3]
# contact = record[0][4]


class NameForm(FlaskForm):
    # email = StringField('Email ID ', [validators.Email(message="invalid email")])
    email = EmailField("Email ",  [InputRequired("Please enter your email address.")])

    submit = SubmitField('Submit')
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    print(session)
    fname = session.get('fname')
    lname = session.get('lname')


    form = NameForm()
    if form.validate_on_submit():
        newemail = form.newemail.data
        print(newemail)

    
    return render_template('profile.html',name=name,sex=sex,email=email,contact=contact,form=form)

