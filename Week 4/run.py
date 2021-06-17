#!/usr/bin/env python3

import os
import json
import requests
from collections import OrderedDict

USER = os.getenv('USER')
desc_direc = '/home/{}/supplier-data/descriptions/'.format(USER)
#desc_direc = os.getcwd() + "/supplier-data/descriptions/"
files = os.listdir(desc_direc)

for filename in files:
    if not filename.startswith('.') and 'txt' in filename:
        with open(desc_direc+filename,'r') as f:
            fb = OrderedDict()
            data = f.readlines()
            fb['name'] = data[0].strip()
            fb['weight'] = int(data[1].split()[0])
            fb['description'] = data[2].strip()
            fb['image_name'] = filename.split('.')[0] + ".jpeg"

            j = json.dumps(fb)
            header = {'Content-Type': 'application/json'}

            r = requests.post("http://localhost/fruits/", headers=header, data=j)
            print(r.status_code)
