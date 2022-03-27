import smtplib
import time
import serial
import socket
import sys
from pymongo import MongoClient
from termcolor import colored
from datetime import datetime

sender = "from@example.com"
receiver = "to@example.com"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    server.login("f69396842d193f", "c831385ef5eec6")
    server.sendmail(sender, receiver, message)