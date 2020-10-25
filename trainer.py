#!/usr/bin/env python
##############################################################################
# Copyright (c) 2012 Hajime Nakagami<nakagami@gmail.com>
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
#
# A image viewer. Require Pillow ( https://pypi.python.org/pypi/Pillow/ ).
##############################################################################
import PIL.Image

try:
    from Tkinter import *
    import tkFileDialog as filedialog
except ImportError:
    from tkinter import *
    from tkinter import filedialog
import PIL.ImageTk
from PIL import Image
import pynder
from helpers import get_access_token, get_login_credentials
from io_helper import save_image
from urllib.request import urlopen
from skimage.io import imread
from bot import like_or_nope
import os
from tensorflow.keras.models import load_model

class App(Frame):
    def get_next_photo(self):
        try:
            self.photo = next(self.photos)
        except StopIteration:
            self.get_next_user()
            self.photos = self.user.get_photos()
            self.photo = next(self.photos)
        except Exception:
            raise

        self.im = Image.open(urlopen(self.photo))
        self.chg_image()


    def get_next_user(self):
        self.suggestion.set("checking ...")
        if hasattr(self, 'user'):
            if self.likes > self.dislikes:
                print('Liked the girl')
                self.user.like()
            else:
                print('Noped the girl')
                self.user.dislike()

        self.likes = 0
        self.dislikes=0
        
        try:
            self.user = next(self.users)
        except StopIteration:
            self.users = self.session.nearby_users()
            self.user = next(self.users)
        except Exception:
            raise

        if hasattr(self, 'model'):
            suggestion = like_or_nope(self.user, self.model)
            self.suggestion.set( f"Suggestion: {suggestion}")
            print(f"AI suggestion: {suggestion}")
        
        self.name.config(text=f"{self.user.name} ({self.user.age})")

    def chg_image(self):
        if self.im.mode == "1": # bitmap image
            self.img = PIL.ImageTk.BitmapImage(self.im, foreground="white")
        else:              # photo image
            self.img = PIL.ImageTk.PhotoImage(self.im)
        self.la.config(image=self.img, bg="#000000", width=self.img.width(), height=self.img.height())
       

    def like_photo(self):
        self.likes += 1
        save_image(imread(self.photo), self.photo, True)
        self.photo_count.set(self.photo_count.get() + 1)
        self.get_next_photo()

    def dislike_photo(self):
        self.dislikes += 1
        save_image(imread(self.photo), self.photo,  False)
        self.photo_count.set(self.photo_count.get() + 1)
        self.get_next_photo()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Tinder swiper')

        email, password, FBID = get_login_credentials()
        FBTOKEN = get_access_token(email, password)
        self.session = pynder.Session(facebook_token=FBTOKEN, facebook_id=FBID)
        self.session.update_location(51.0543, 3.7174)

        fram = Frame(self)
        Button(fram, text="Yes", command=self.like_photo).pack(side=LEFT)
        Button(fram, text="Nope", command=self.dislike_photo).pack(side=LEFT)
        self.name = Label(fram, text='')
        self.name.pack(side=LEFT)

        self.photo_count = IntVar()
        self.photo_count.set(sum(len(files) for _, _, files in os.walk(r'./validation')))


        Label(fram, text="Total photos: ").pack(side=LEFT)
        Label(fram, textvariable=self.photo_count).pack(side=LEFT)

        self.suggestion = StringVar()
        Label(fram, textvariable=self.suggestion).pack(side=LEFT)
       
        fram.pack(side=TOP, fill=BOTH)
        self.la = Label(self)
        self.la.pack()

        model_file = "model_V4.h5"
        if os.path.isfile(model_file):
            model = load_model("model_V4.h5")
            self.model = model

        # setup inital setuff
        self.likes = 0
        self.dislikes=0
        self.users = self.session.nearby_users()
        self.get_next_user()
        self.photos = self.user.get_photos(width=640)
        self.get_next_photo()




        self.pack()

if __name__ == "__main__":
    app = App(); app.mainloop()