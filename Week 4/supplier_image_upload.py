#!/usr/bin/env python3

import requests
import os

url = "http://localhost/upload/"
USER = os.getenv('USER')
directory = '/home/{}/supplier-data/images/'.format(USER)
files = os.listdir(directory)

for name in files:
    if not name.startswith('.') and 'jpeg' in name:
        path = directory + name
        with open(path, 'rb') as f:
            r = requests.post(url, files={'file': f})
