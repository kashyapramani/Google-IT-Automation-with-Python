#!/usr/bin/env python3

import socket
import shutil
import psutil
import emails
import os


USER = os.getenv('USER')
sender = "automation@example.com"
receiver = "{}@example.com".format(USER)
body = "Please check your system and resolve the issue as soon as possible."


def send_email(sub):
    email = emails.generate_error_email(sender, receiver, sub, body)
    emails.send(email)


def check_cpu_usage():
    usage = psutil.cpu_percent(1)
    return usage > 80


def check_disk_usage(disk):
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free < 20


def check_memory_usage():
    mu = psutil.virtual_memory().available
    total = mu / (1024.0 ** 2)
    return total < 500


def check_localhost():
    localhost = socket.gethostbyname('localhost')
    return localhost == "127.0.0.1"


if check_cpu_usage() :
    subject = "Error - CPU usage is over 80%"
    print(subject)
    send_email(subject)

if check_memory_usage():
    subject = "Error - Available memory is less than 500MB"
    print(subject)
    send_email(subject)

if check_disk_usage('/'):
    subject = "Error - Available disk space is less than 20%"
    print(subject)
    send_email(subject)

if not check_localhost():
    subject = "Error - localhost cannot be resolved to 127.0.0.1"
    print(subject)
    send_email(subject)

