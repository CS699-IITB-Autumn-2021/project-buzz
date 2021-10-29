import random
from twilio.rest import Client
from flask import session
from App import config


def generateOTP():
    """
    This function generates a 6 digit random number

    Returns:
        ::6 digit random number
    """
    return random.randrange(100000, 999999)


def getOTPApi(number):
    """
    This function sends the OTP to the clients by accessing TWILIO messaging service

    Inputs:
        :number: Phone number entered by the user
        :type number: String

    Returns:
        ::A boolean variable specifying status of message sent by backend, TRUE if sent successfully else FALSE
    """
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
