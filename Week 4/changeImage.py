#!/usr/bin/env python3

from PIL import Image
import os


USER = os.getenv('USER')
directory = '/home/{}/supplier-data/images/'.format(USER)
files = os.listdir(directory)


for name in files:

    if not name.startswith('.') and 'tiff' in name:
        im_path = directory + name
        im = Image.open(im_path)

        path = os.path.splitext(im_path)[0]
        new_path = '{}.jpeg'.format(path)

        im.convert('RGB').resize((600, 400)).save(new_path, "JPEG")
