#!/usr/bin/env python3

import os
import requests
from collections import OrderedDict


path = "/data/feedback/"
files = os.listdir(path)


for file in files:
    with open(os.path.join(path, file), 'r') as f:

        data = f.readlines()

        fb = OrderedDict()

        fb["title"] = data[0].strip()
        fb["name"] = data[1].strip()
        fb["date"] = data[2].strip()
        fb["feedback"] = data[3].strip()

        header = {'Content-Type': 'application/json'}
        res = requests.post("http://35.193.29.249/feedback/",headers=header, json=fb)

        print(res.ok)
        print(res.status_code)
