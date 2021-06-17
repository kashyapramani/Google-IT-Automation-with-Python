#!/usr/bin/env python3

import os
import datetime
import reports
import emails


def take_data(desc_direc):

    files = os.listdir(desc_direc)
    fruit_names = []
    fruit_weight = []

    for filename in files:
        if not filename.startswith('.') and 'txt' in filename:
            with open(desc_direc + filename, 'r') as f:
                data = f.readlines()
                name = data[0].strip()
                weight = data[1]

                fruit_names.append(name)
                fruit_weight.append(weight)

    content = ""
    br = "<br/>"

    for name, weight in zip(fruit_names,fruit_weight):
        content += "name: " + name + br + "weight: " + weight + br + br

    return content


if __name__ == "__main__":
    USER = os.getenv('USER')
    directory = '/home/{}/supplier-data/descriptions/'.format(USER)

    date = datetime.date.today().strftime("%B %d, %Y")

    title = 'Processed Update on ' + str(date)
    path = "/tmp/processed.pdf"

    reports.generate(path, title, take_data(directory))

    sender = "automation@example.com"
    receiver = "{}@example.com".format(USER)
    subject = 'Upload Completed - Online Fruit Store'
    body = 'All fruits are uploaded to our website successfully. A detailed list is attached to this email.'

    msg = emails.generate(sender, receiver, subject, body, path)
    emails.send(msg)
