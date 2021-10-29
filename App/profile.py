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
# cur.execute("""SELECT  first_name,last_name,sex.name,email,contact_no FROM user,sex  WHERE user_id='1' and user.sex_id = sex.id """)


# record = cur.fetchall()
# for data in record:
#     print(data)
# print(record)
# fname = record[0][0]
# print(type(record))
# lname = record[0][1]
# name = fname+" "+lname
# sex = record[0][2]
# email = record[0][3]
# contact = record[0][4]

# name = "tempname"
# sex = "female"
# email = "abc@fmailo.com"
# contact = "9876543210"


class updateEmailForm(FlaskForm):
    """
    [This function ]

    :param FlaskForm: [description]
    :type FlaskForm: [type]
    """
    # email = StringField('Email ID ', [validators.Email(message="invalid email")])
    email = EmailField("Email ",  [InputRequired("Please enter your email address.")])

    submit = SubmitField('Submit')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    [This function is used to extract user data for profile page.If no user is logged in it will redirect to login page/home page]

    :param FlaskForm: [description]
    :type FlaskForm: [type]
    """
    userid = session.get('userId')
    if(userid == None):
        return redirect('/')
    print(session)
    # fname = session.get('first_name')
    # lname = session.get('last_name')
    # print("last name is ",lname)
    finalData = session.get('finalData')
    fname = finalData['first_name']
    # print("hey my name is ",fname)
    lname = finalData['last_name']
    name = fname + " " + lname
    email = finalData['email']
    sex = finalData['sex']
    contact = session.get('number')






    print(finalData)


    form = updateEmailForm()
    if form.validate_on_submit():
        
        newemail = form.newemail.data
        cur.execute("""Update user set email = $[newemail] where user_id = $[userId] """)
        finalData = session.get('finalData')
        finalData['email'] = newemail 
        session['finalData'] = finalData
        print("newwwwww sesssion",session)
        


       
        
       

    
    return render_template('profile.html',fname=fname,name=name,sex=sex,email=email,contact=contact,form=form)

