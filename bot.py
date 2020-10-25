from skimage.io import imread, imsave, imshow, show
import matplotlib.pyplot as plt
import pynder
from helpers import get_access_token, get_login_credentials
from io_helper import save_image
from time import sleep
from random import randint
from messages import messages
from image_processing import extract_faces
import numpy as np
from tensorflow.keras.models import load_model
import random

# random bugfixes
import tensorflow as tf
gpu = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpu[0], True)


def check_swipes(session):
    '''
    INPUT:
    ACTION: Will check if I still have swipes
    OUTPUT:
    '''
    swipes_remaining = session.likes_remaining
    if swipes_remaining == 0:
        return 'Send messages'

def like_or_nope(user, compiled_model):
    '''
    INPUT: Image file
    OUTPUT: Like or Dislike
    '''
    photos = user.get_photos()

    print("Fetched user photos..")
    likes = 0
    dislikes = 0
    total = 0

    for photo in photos:
        total += 1
        image = imread(photo)
        # imshow(image) # Shows image of person
        # show()
        face = np.array(extract_faces(image))
        if len(face) != 0:
            prediction = compiled_model.predict(face) # Add the model file here instead
            if prediction[0][1] > 0.4:
                likes += 1
            else:
                dislikes += 1
        else:
            print("AI cannot tell from photo. Retrieving next photo")

    print(f"Of all fetched {total} photos I (the AI) like a total of {likes} photos and disliked {dislikes}")
    if likes > dislikes:
        return "like"
    else:
        return "dislike"

def swipe(session,model,n):
    '''
    INPUT: Session object, nearby users object
    ACTION: Will swipe until swipe limit is reached.
        - Currently swiping at random
    OUTPUT:
    '''
    total_swipes = n
    likes = 0
    dislikes = 0
    while total_swipes !=0 :
        users = session.nearby_users()
        try:
            for user in users:
                print("Checking Swipes remaining.....")
                status = check_swipes(session)
                if total_swipes == 0 or status == 'Send messages':
                    print("For this session, I've swiped right on " + str(likes) + " people.")
                    print("For this session, I've swiped left on " + str(dislikes) + " people.")
                    print("You've reached the swipe limit. AI will now start sending messages to matches")
                    break
                else:
                    action = like_or_nope(user, model)
                    # print("Remaining Swipes: " + str(n))
                    if action == 'like':
                        user.like()
                        total_swipes -= 1
                        likes += 1
                        for photo in user.photos:
                            image = imread(photo)
                            save_image(image, photo, False, 'bot', f"{user.name}_{user.id}")
                        print('The Bae-ta Miner liked ' + user.name + '! Wohoooo!!!!!!!')
                        print('-------------------------------------------------------')
                        sleep(randint(3,15))
                    else:
                        user.dislike()
                        total_swipes -= 1
                        dislikes += 1
                        for photo in user.photos:
                            image = imread(photo)
                            save_image(image, photo, False, 'bot',  f"{user.name}_{user.id}")
                        print('The Bae-ta Miner disliked ' + user.name+ ' *Sad Face*')
                        print('-------------------------------------------------------')
                        sleep(randint(3,15))
        except:
            print("Error Occured. Bot will try again.")



def send_message(session):
    '''
    INPUT: Session object
    ACTION: Will send an automated message to whomever I match with.
    OUTPUT:
    '''
    matches = session.matches()
    for match in matches:
        to_send_message = random.choice(messages)
        print("Sending message: " + to_send_message)
        match.message(to_send_message)

if __name__=='__main__':
    print('Hi Jeff. Im the Bae-ta Miner. I know the online dating process is a huge hassle.')
    print('Im here to help! Im here to automate the process for you.')

    print('-----------------------------------------------------------------------------')
    print('First, Ill need to get your login credentials from your Facebook account.')
    ## Get Login Credentials
    email, password, FBID = get_login_credentials()
    FBTOKEN = get_access_token(email, password)

    print('-----------------------------------------------------------------------------')
    print('Now, I will start your Tinder session.')
    print('Starting Tinder Session........')
    print('Tinder session started!')
    ## Start Tinder Session
    session = pynder.Session(facebook_token=FBTOKEN, facebook_id=FBID)

    print('-----------------------------------------------------------------------------')
    print('Loading model..............')
    model = load_model("model_V4.h5")

    print('-----------------------------------------------------------------------------')
    ## Swipe Through users
    print('How many times would you like me to swipe this session?')
    total_swipes = int(input())

    swipe(session, model, total_swipes)
    # print('-----------------------------------------------------------------------------')
    # print('Now, sending automated messages to current matches........')

    ## Send messages to the matches
    # send_message(session)

    print('You have Tindered for the day. Have a great day!')
