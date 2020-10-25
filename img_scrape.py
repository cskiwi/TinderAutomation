from skimage.io import imread, imsave, imshow, show
import matplotlib.pyplot as plt
import pynder
from helpers import get_access_token, get_login_credentials
from io_helper import save_image
from PIL import Image
import requests
from selenium import webdriver
import os, os.path
from tkinter import *

email, password, FBID = get_login_credentials()
FBTOKEN = get_access_token(email, password)
session = pynder.Session(facebook_token=FBTOKEN, facebook_id=FBID)
driver = webdriver.Chrome('.\chromedriver.exe')


while True:
    users = session.nearby_users()
    input_string = "Write 1 to like. Write 2 to dislike."
    for user in users:
        photos = user.get_photos()
        print("Fetched user photos..")
        print("User", user.common_likes)
        for photo in photos:
            image = imread(photo)
            driver.get(photo)
            
            ans = str(input(input_string)).lower()

            if ans == "1":
                save_image(image, photo, True)
            else:
                save_image(image, photo, False)
