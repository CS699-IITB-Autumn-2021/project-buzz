import random
from twilio.rest import Client
from flask import session
from App import config


# generating a random six digit number for OTP
def generateOTP():
    return random.randrange(100000, 999999)


# sending OTP message to the client
def getOTPApi(number):
    account_sid = config["TWILIO_ACCOUNT_SID"]
    auth_token = config["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    otp = generateOTP()
    session['response'] = str(otp)
    body = 'Your OTP is ' + str(otp)
    message = client.messages.create(
        from_=config["TWILIO_VIRTUAL_NUMBER"],
        body=body,
        to=number
    )

    if message.sid:
        return True
    else:
        return False
