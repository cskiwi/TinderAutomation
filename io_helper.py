from skimage.io import imsave
import os
import sys

base_folder = "validation"

def save_image(image, name, liked, filename = base_folder, user_name = ""):
    if liked:
        filename += "/likes/"
    else:
        filename += "/dislikes/"

    if len(user_name) != 0:
        filename+= f"{user_name}/"

    if not os.path.exists(filename):
        os.makedirs(filename)

    file_url_list = name.split("/")
    filename += file_url_list[-1]
    print(filename)
    imsave(filename, image)
