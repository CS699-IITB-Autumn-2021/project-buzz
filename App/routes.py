from flask import request, render_template, flash, url_for
from App import app
from App.sso import *
from App.otp import *
from App.forms import PhoneNumberForm
from App import conn, cur
from App.chatDBOperations import *
#my imports
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email

@app.route('/')
def ssoVerification():
    # Error handling page redirection
    if "error" in request.args.keys():
        return "Something went wrong"

    # If login url does not have code then ask user to authenticate using SSO
    if "code" not in request.args.keys():
        url = createRegisterURL()
        return redirect(url)
    code = request.args['code']

    # Getting access token and refresh token
    creds = fetchCredentials(code)
    if type(creds) == type(redirect("/")):
        return creds

    # Getting user data using credentials
    userData = getData(creds["access_token"],
                       "fields=first_name,last_name,type,profile_picture,sex,username,email,program,contacts,insti_address,secondary_emails,mobile,roll_number")

    # Checking if all required data is available
    required = ["username", "email", "first_name", "last_name", "sex"]
    for field in required:
        if field not in userData.keys():
            return redirect("/?error=Please give all permissions")

    # Massaging data
    finalData = {}
    finalData = userData
    finalData["roll_number"] = userData["username"]
    finalData.pop("id")
    finalData.pop("username")
    finalData.pop("type")
    session['finalData'] = finalData

    # checking if user already exists
    # change to appropriate redirection link later at present only flashing a message
    cur.execute("SELECT * FROM user")
    records = cur.fetchall()
    for rows in records:
        if rows[0] == finalData['roll_number']:
            return "User already exits direct them to post-login landing page straight away"
    # return finalData
    # return render_template('enter_phone_number.html')
    return redirect(url_for('getOTP'))


@app.route('/getOTP', methods=['POST', 'GET'])
def getOTP():
    # fetching the phone number and validating it
    form = PhoneNumberForm()
    if form.validate_on_submit():
        number = form.contact_no.data
        session['number'] = number
        val = getOTPApi(number)
        if val:
            return render_template("enterOTP.html")
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('enter_phone_number.html', form=form)


@app.route('/validateOTP', methods=['POST', 'GET'])
def validateOTP():
    otp = request.form['otp']
    finalData = session.get('finalData')
    valid = True
    phone_number = session.get('number')
    if 'response' in session:
        s = session['response']
        if s == otp:
            '''
            # checking if user already exists
            # change to appropriate redirection link later at present only flashing a message
            cur.execute("SELECT * FROM user")
            records = cur.fetchall()
            for rows in records:
                if rows[0] == finalData['roll_number']:
                    flash(f'User already exists:', category='danger')
                    return render_template('enterOTP.html')
            '''
            # inserting the user if he new to the website
            query = """INSERT INTO user(user_id, first_name, last_name, email, contact_no, roll_no, valid) VALUES(?,?,?,?,?,?,?) """
            data = [finalData['roll_number'], finalData['first_name'], finalData['last_name'], finalData['email'], int(phone_number[1:]), int(finalData['roll_number']), valid]
            cur.execute(query, data)
            conn.commit()
            '''
            cur.execute("SELECT * FROM user")
            records = cur.fetchall()
            for rows in records:
                print(rows[0])
            print(finalData)
            flash(f'User Created Successfully:', category='success')
            '''
            # return render_template('enterOTP.html')
            return "First time login user successfully added to database, phone number also verified, redirect user to post-login landing page straight away"
        else:
            flash(f'Wrong OTP:', category='danger')
            return render_template('enterOTP.html')


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    finalData = session.get('finalData')
    username = finalData['first_name'] + " " + finalData['last_name']

    # static rooms are defined in the below array: need to replace the list to a dynamic one
    # ROOMS = ['lounge', 'news', 'games', 'coding']
    ROOMS = []
    finalData = session.get("finalData")
    currentUser = finalData['first_name'] + " " + finalData['last_name']
    list_of_rooms = get_rooms_for_user(currentUser)
    for room in list_of_rooms:
        ROOMS.append(room['room_name'])
    return render_template('chat.html', username=username, rooms=ROOMS)


# dummy login for the test user - remove this once all testing is done
@app.route("/dummylogin", methods=['GET', 'POST'])
def dummyLogin():
    cur.execute("""SELECT * FROM user WHERE user_id='test-rollnumber' """)
    records = cur.fetchall()
    print(records[0])
    finalData = {}
    finalData['user_id'] = records[0][0]
    finalData['first_name'] = records[0][1]
    finalData['last_name'] = records[0][2]
    finalData['email'] = records[0][3]
    finalData['contact_no'] = records[0][4]
    finalData['sex_id'] = records[0][5]
    finalData['roll_no'] = records[0][6]
    session['finalData'] = finalData
    for rows in records:
        print(rows)
    return redirect(url_for('chat'))


@app.route("/dummylogin1", methods=['GET', 'POST'])
def dummyLogin1():
    cur.execute("""SELECT * FROM user WHERE user_id='test-rollnumber1' """)
    records= cur.fetchall()
    print(records[0])
    finalData = {}
    finalData['user_id'] = records[0][0]
    finalData['first_name'] = records[0][1]
    finalData['last_name'] = records[0][2]
    finalData['email'] = records[0][3]
    finalData['contact_no'] = records[0][4]
    finalData['sex_id'] = records[0][5]
    finalData['roll_no'] = records[0][6]
    session['finalData'] = finalData
    for rows in records:
        print(rows)
    return redirect(url_for('chat'))


@app.route("/dummylogin2", methods=['GET', 'POST'])
def dummyLogin2():
    cur.execute("""SELECT * FROM user WHERE user_id='test-rollnumber2' """)
    records = cur.fetchall()
    print(records[0])
    finalData = {}
    finalData['user_id'] = records[0][0]
    finalData['first_name'] = records[0][1]
    finalData['last_name'] = records[0][2]
    finalData['email'] = records[0][3]
    finalData['contact_no'] = records[0][4]
    finalData['sex_id'] = records[0][5]
    finalData['roll_no'] = records[0][6]
    session['finalData'] = finalData
    for rows in records:
        print(rows)
    return redirect(url_for('chat'))


@app.route("/dummylogin3", methods=['GET', 'POST'])
def dummyLogin3():
    cur.execute("""SELECT * FROM user WHERE user_id='test-rollnumber3' """)
    records = cur.fetchall()
    print(records[0])
    finalData = {}
    finalData['user_id'] = records[0][0]
    finalData['first_name'] = records[0][1]
    finalData['last_name'] = records[0][2]
    finalData['email'] = records[0][3]
    finalData['contact_no'] = records[0][4]
    finalData['sex_id'] = records[0][5]
    finalData['roll_no'] = records[0][6]
    session['finalData'] = finalData
    for rows in records:
        print(rows)
    return redirect(url_for('chat'))


# dummy route to pass in the product owner name to the create room stuff
# this in final must accept only POST request from the View-single-commodity-page(Wireframe reference) and must pass in
# product owner name
@app.route("/create-room", methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        owner_name = request.form.get("owner")
        print(owner_name)
        finalData = session.get("finalData")
        currentUser = finalData['first_name'] + " " + finalData['last_name']
        list_of_rooms = get_rooms_for_user(currentUser)
        for room in list_of_rooms:
            if is_room_member(room['_id']['room_id'], owner_name):
                return redirect(url_for("chat"))
        roomname = currentUser + " " + owner_name + " chat room"
        saveRoom(roomname, currentUser, owner_name)
        return redirect(url_for("chat"))
    return render_template("create-room.html")

    