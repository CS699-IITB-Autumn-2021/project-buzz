import requests
from werkzeug.utils import redirect
from App import config


def createRegisterURL():
    '''Create a URL to authorize used'''
    return config["SSO_URL"] + "?" + "client_id=" + config["CLIENT_ID"] + "&response_type=code&scope=" + config[
        "scope"] + "&redirect_uri=" + config["REDIRECT_URI"]


def fetchCredentials(code):
    '''fetch access token and refesh token'''

    header = {
        "Authorization": config["CREDENTIALS_TOKEN"]
    }
    data = {
        "code": code,
        "grant_type": "authorization_code",
    }

    response = requests.post(config["CREDENTIALS_FETCH_URL"], data=data, headers=header).json()

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
        "Authorization": config["CREDENTIALS_TOKEN"]
    }
    data = {
        "refresh_token": refreshToken,
        "grant_type": "refresh_token",
    }
    response = requests.post(config["CREDENTIALS_FETCH_URL"], data=data, headers=header).json()

    # Providing only usefull data
    creds = {}
    creds["refresh_token"] = response["refresh_token"]
    creds["access_token"] = response["access_token"]
    print(creds["access_token"])
    return creds


def getData(accessToken, params):
    '''fetch the data required to register user like - first name,last name,sex etc'''
    header = {
        "Authorization": "Bearer " + accessToken
    }
    params = "?" + str(params)
    response = requests.get(config["DATA_URL"] + params, headers=header).json()
    # print(params, header)
    return response