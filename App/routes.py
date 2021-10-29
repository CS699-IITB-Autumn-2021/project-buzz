from flask import request, render_template, flash, url_for
from App import app
from App.sso import *
from App.otp import *
from App.forms import PhoneNumberForm
from App import conn, cur
from App.chatDBOperations import *
# my imports
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import InputRequired, Email

from App.bingoClassifiedDbCode import seedDB
import uuid

seedDB()


# conn.close()


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    [Function to redirect to index page of webapp]

    
    """
    userid = session.get('userId')
    print("userid", userid)
    if userid == None:
        userid = ""

    return render_template('index.html', userid=userid)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    [Function to clear session and redirect to index page]

    
    """
    userid = session.get('userId')
    userid = ""

    session.clear()

    return redirect('/')


# @app.route('/header', methods=['GET', 'POST'])
# def header():
#     finalData = session.get('finalData')
#     fname = finalData['first_name']
#     return render_template('header.html',fname=fname)


class addBidForm(FlaskForm):
    """
    [Function to take input bid from user]

    :param FlaskForm: [Takes integerfield bid as input]
    
    """
    # email = StringField('Email ID ', [validators.Email(message="invalid email")])
    bid = IntegerField("BID ",  [InputRequired("add your bid here")])

    submit = SubmitField('Submit')


class userRatingForm(FlaskForm):
    """
    [Function to take input user rating from user]

    :param FlaskForm: [takes integerfield rating as input]
    
    """
    # email = StringField('Email ID ', [validators.Email(message="invalid email")])
    rating = IntegerField("User Rating ",  [InputRequired("Put user rating here"),NumberRange(min=0, max=10, message='Please insert value between 0 and 10')])
    submit = SubmitField('Submit')

@app.route('/viewProducts/detail/<productId>', methods=['GET', 'POST'])
def detail(productId):
    
    #cur.execute("""Insert into products values(NULL,2,"1","A good book in good condition",500,"BOOK",2,100,4,0,1,1,20,NULL,NULL,NULL) """)
    
    """
    [This function extract all the data for detail page and renders it.]

    
    """
    id = productId
    print("id id id is here",id)
    cur.execute("Select * from products  where id=\'%s\' "%(id))
    details = cur.fetchall()
    userId = details[0][2]
    cur.execute("Select * from user  where user_id=\'%s\' "%(userId))
    userdetails = cur.fetchall()
    # print("here are details",details,userdetails)
    description = details[0][3]
    price = details[0][4]
    title=details[0][5]
    contact_no=""
    contact_no = userdetails[0][4]
    postedon = details[0][13]
    seller=""
    seller = userdetails[0][1] + " "+ userdetails[0][2]
    cur.execute("Select image_url from images  where product_id=\'%s\' "%(id))
    images = cur.fetchall()
    sellingOption = details[0][10]
    seller = userdetails[0][1] + " "+ userdetails[0][2]
    print("sell option",sellingOption)
    cur.execute("Select avg(rating) from rating  where user_id=\'%s\' "%(userId))
    showRatingValue = cur.fetchall()[0][0]
    print(showRatingValue)
    # return ("your product id"+productId)
    form= addBidForm()
    ratingForm = userRatingForm()
    if ratingForm.validate_on_submit():
        rating = ratingForm.rating.data
        print("your bid is ",rating)
        userid=session.get('userId')
        cur.execute("Insert into rating(user_id,rating) values(\'%s\',%d) "%(userId,rating))
        cur.execute("select * from rating")
        record = cur.fetchall()
        print("here is our rating entry",record)
    if form.validate_on_submit():
        bid = form.bid.data
        print("your bid is ",bid)
        userid=session.get('userId')
        cur.execute("Insert into bid(product_id,user_id,bid_price) values(\'%s\','%s\','%s\') "%(id,userid,bid))
        cur.execute("select * from bid")
        record = cur.fetchall()
        print("here is our bid entry",record)
        conn.commit()
    
    return render_template('detail.html',showRatingValue=showRatingValue ,images=images,description =description,price =price,title=title,contact_no=contact_no ,sellingOption=sellingOption,postedon=postedon ,seller=seller,form=form,userRating= ratingForm
)


@app.route('/sso')
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
            # inserting the user if he new to the website
            sexData = {}
            sexData["female"] = 1
            sexData["male"] = 2
            sexData["other"] = 3

            # sexData = {val:key for key,val in records}
            userSex = 1
            print("dict", sexData)
            print("heyyyyyyyyyyy", finalData["sex"])
            if finalData["sex"]:
                userSex = sexData[finalData["sex"]]
            userId = str(uuid.uuid4())
            session["userId"] = userId
            print(finalData, phone_number, type(phone_number), int(phone_number[3:]))
            query = """INSERT INTO user(user_id, first_name, last_name, email, contact_no, roll_no, valid) VALUES(?,?,?,?,?,?,?) """
            data = [userId, finalData['first_name'], finalData['last_name'], finalData['email'], (phone_number[3:]),
                    int(finalData['roll_number']), valid]
            cur.execute(query, data)
            conn.commit()
            return redirect(url_for('home'))
        else:
            flash(f'Wrong OTP:', category='danger')
            return render_template('enterOTP.html')


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    userid = session.get('userId')
    if (userid == None):
        return redirect('/')
    finalData = session.get('finalData')
    username = finalData['first_name'] + " " + finalData['last_name']
    ROOMS = []
    list_of_rooms = get_rooms_for_user(username)
    for room in list_of_rooms:
        ROOMS.append(room['room_name'])
    return render_template('chat.html', username=username, rooms=ROOMS)


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



@app.route('/updatePhoneNumber', methods=['POST', 'GET'])
def updatePhoneNumber():
    userid = session.get('userId')
    if (userid == None):
        return redirect('/')
    # fetching the phone number and validating it
    form = PhoneNumberForm()
    if form.validate_on_submit():
        number = form.contact_no.data
        # if the phone number of the user is same as earlier number, then flash a message to provide another number
        if number == session['number']:
            flash(f'This is your current number please enter a different one', category='danger')
            return render_template('enter_phone_number.html', form=form)
        session['number'] = number
        val = getOTPApi(number)
        if val:
            return render_template("UpdatePhoneOTP.html")
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error in updating phone number: {err_msg}', category='danger')
    return render_template('enter_phone_number.html', form=form)


@app.route('/validateOTPForUpdate', methods=['POST', 'GET'])
def validateOTPForUpdate():
    userid = session.get('userId')
    if (userid == None):
        return redirect('/')
    otp = request.form['otp']
    phone_number = session.get('number')
    phone_number = (phone_number[3:])
    if 'response' in session:
        s = session['response']
        if s == otp:
            cur.execute("""Update user set contact_no = ? where user_id = ? """, (phone_number, userid))
            conn.commit()
            return redirect(url_for('profile'))
        else:
            flash(f'Wrong OTP:', category='danger')
            return render_template('UpdatePhoneOTP.html')


@app.route("/dummylogin3", methods=['GET', 'POST'])
def dummyLogin3():
    query = """INSERT INTO user(user_id, first_name, last_name, email, contact_no, roll_no, valid) VALUES(?,?,?,?,?,?,?) """
    data = ['test-rollnumber3', 'Test', 'User', 'test3@gmail.com', 919876543217, 12348, True]
    cur.execute(query, data)
    conn.commit()
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