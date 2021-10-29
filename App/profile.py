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






class updateEmailForm(FlaskForm):
    """
    [This function is used to update email ]

    :param FlaskForm: [description]
    :type FlaskForm: [type]
    """
     
    email = EmailField("Email ",  [InputRequired("Please enter your email address.")])

    submit = SubmitField('Submit')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    [This function is used to extract user data for profile page.If no user is logged in it will redirect to login page/home page.]

    
    
    """
    userid = session.get('userId')
    if(userid == None):
        return redirect('/')
    print(session)
    #getting data stored in session
    finalData = session.get('finalData')
    fname = finalData['first_name']
    
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

