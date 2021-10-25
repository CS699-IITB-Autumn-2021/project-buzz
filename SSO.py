from dotenv import dotenv_values 
from flask import Flask,request
import requests
from werkzeug.utils import redirect
app = Flask(__name__)
config = dotenv_values(".env") 

def createRegisterURL():
	'''Create a URL to authorize used'''

	return config["SSO_URL"]+"?"+"client_id="+config["CLIENT_ID"]+"&response_type=code&scope="+config["scope"]+"&redirect_uri="+config["REDIRECT_URI"]

def fetchCredentials(code):
	'''fetch access token and refesh token'''

	header = {
		"Authorization":config["CREDENTIALS_TOKEN"]
	}
	data ={
		"code":code,
		"grant_type":"authorization_code",
	}

	response = requests.post(config["CREDENTIALS_FETCH_URL"],data=data,headers=header).json()
	
	if "error" in response.keys():
		if response["error"] == "invalid_grant":
			print("igopt jhteter")
			return redirect("/")
		return redirect("/?error=lol")

	# Providing only usefull data
	creds = {}
	creds["refresh_token"] = response["refresh_token"]
	creds["access_token"] = response["access_token"]	

	return creds

def accessTokenRefresh(refreshToken):
	header = {
		"Authorization":config["CREDENTIALS_TOKEN"]
	}
	data ={
		"refresh_token":refreshToken,
		"grant_type":"refresh_token",
	}
	response = requests.post(config["CREDENTIALS_FETCH_URL"],data=data,headers=header).json()

	# Providing only usefull data
	creds = {}
	creds["refresh_token"] = response["refresh_token"]
	creds["access_token"] = response["access_token"]	
	print(creds["access_token"])
	return creds	

def getData(accessToken,params):
	'''fetch the data required to register user like - first name,last name,sex etc'''
	header = {
		"Authorization": "Bearer "+ accessToken
	}
	params = "?"+str(params)
	response = requests.get(config["DATA_URL"]+params,headers=header).json()
	print(params,header)
	return response

@app.route('/')
def ssoVerification():
	# Error handling page redirection
	if "error" in request.args.keys():
		return "Something went wrong"
	
	# If login url does not have code then ask user to authenticate using SSO
	if "code" not in request.args.keys():
		url  = createRegisterURL()
		return redirect(url)
	code = request.args['code']

	# Getting access token and refresh token
	creds = fetchCredentials(code)
	if type(creds) == type(redirect("/")):
			return creds
	
	# Getting user data using credentials 
	userData = getData(creds["access_token"],"fields=first_name,last_name,type,profile_picture,sex,username,email,program,contacts,insti_address,secondary_emails,mobile,roll_number")
	
	# Checking if all required data is available
	required = ["username","email","first_name","last_name","sex"]
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


	return finalData

if __name__ == '__main__':
	app.run(debug=True)