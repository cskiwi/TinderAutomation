import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

import robobrowser
import re
import json
import os
import random
import requests

MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"

def get_access_token(email, password):
    browser = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    browser.open(FB_AUTH)
    form = browser.get_form()
    form["pass"] = password
    form["email"] = email
    browser.submit_form(form)
    form = browser.get_form()
    try:
        browser.submit_form(form, submit=form.submit_fields['__CONFIRM__'])
        access_token = re.search(
            r"access_token=([\w\d]+)", browser.response.content.decode()).groups()[0]
        return access_token
    except requests.exceptions.InvalidSchema as browserAddress:
        access_token = re.search(
            r"access_token=([\w\d]+)", str(browserAddress)).groups()[0]
        return access_token
    except Exception as ex:
        print("access token could not be retrieved. Check your username and password.")
        print("Official error: %s" % ex)
        return {"error": "access token could not be retrieved. Check your username and password."}

def get_login_credentials():
    print("Checking for credentials..")
    if os.path.exists('auth.json'):
        print("Auth.json existed..")
        with open("auth.json") as data_file:
            data = json.load(data_file)
            if "email" in data and "password" in data and "FBID" in data:
                return (data["email"], data["password"], data["FBID"])
            else:
                print ("Invalid auth.json file")

    print ("Auth.json missing or invalid. Please enter your credentials.")
    return (input("Enter email ..\n"), input("Enter password..\n"))
