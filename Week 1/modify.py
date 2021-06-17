#!/usr/bin/env python3

from PIL import Image
import os


size = (128, 128)
path = os.getcwd() + "/images/"
files = os.listdir(path)
for f in files:
    if "ic_" in f:
        im = Image.open(path+f).convert('RGB')
        im.rotate(270).resize(size).save("/opt/icons/" + f, "JPEG")

