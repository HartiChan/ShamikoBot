# coding=utf-8

# Copyright (c) 2020 HartiChan

#   .d8888b.  888                             d8b 888                       .d8888b.                888          
#  d88P  Y88b 888                             Y8P 888                      d88P  Y88b               888          
#  Y88b.      888                                 888                      888    888               888          
#   "Y888b.   88888b.   8888b.  88888b.d88b.  888 888  888  .d88b.         888         .d88b.   .d88888  .d88b.  
#      "Y88b. 888 "88b     "88b 888 "888 "88b 888 888 .88P d88""88b        888        d88""88b d88" 888 d8P  Y8b 
#        "888 888  888 .d888888 888  888  888 888 888888K  888  888 888888 888    888 888  888 888  888 88888888 
#  Y88b  d88P 888  888 888  888 888  888  888 888 888 "88b Y88..88P        Y88b  d88P Y88..88P Y88b 888 Y8b.     
#   "Y8888P"  888  888 "Y888888 888  888  888 888 888  888  "Y88P"          "Y8888P"   "Y88P"   "Y88888  "Y8888  
#   

from Core.Shamiko import telegram_chatbot
from Utils import Logger as Log

import operator
import re
import time
import random
import sys
import psutil
import json

class yuko_trigger:

    def make_reply(self, msg):
        reply = None
    
        if msg is not None:
            Log.i(msg)

            if msg == "ping":
                Log.a("pong")
                reply = "pong"

            if msg == "info":
                Log.a("Shamiko-Project, version 0.0.3.1")
                reply = "Shamiko-Project, version 0.0.3.1"



        return reply

    def make_tag(self, msg, username):

        if msg is not None:

            if msg == "hello" + " there":
                Log.a("Hello there")
                reply = "Hello @" + username + ". I am Yuko ( ^ ω ^)"

            if msg == "Hi" or "hi" or "Hello" or "hello":
                Log.a("Hello")
                reply = "Hi @" + username + " ^^"
        
        return reply
        
    def make_reply_name(self, msg, first_name):

        if msg is not None:

            if msg == "test":
                Log.a("test")
                reply = "test " + first_name

        return reply

    def reply_to_usermessage(self, msg, sendname, takename):

        if msg is not None:

            if msg == "yuko pat her":
                Log.a("pat her")
                reply = "Hai! *smiles and jumps on " + takename + "'s arms*"
        
        return reply




