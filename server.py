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
from Core.Dialoger import yuko_trigger

import operator
import re
import time
import random
import sys
import psutil
import json


bot = telegram_chatbot("config.cfg")
trigger = yuko_trigger()

bot.sendbootmsg("Booted!")
Log.i("Starting Shamiko-Project, version 0.0.3.1")

update_id = None

while True:

    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    print(updates)
    print(update_id)

    if updates:

        for item in updates:

            update_id = item["update_id"]
            try:
 
                message = str(item["message"]["text"])
 
            except:
 
                message = None
 
            from_ = item["message"]["from"]["id"]
            chat_ = item["message"]["chat"]["id"]
            username_ = item["message"]["from"]["username"]
            first_name_ = item["message"]["from"]["first_name"]
                

            Log.i(from_)
            Log.i(chat_)

            if from_ == chat_:
                reply = trigger.make_reply(message)
                reply = trigger.make_tag(message, username_)
                reply = trigger.make_reply_name(message, first_name_)
                bot.send_message(reply, from_)

            if from_ != chat_:
                reply = trigger.make_reply(message)
                reply = trigger.make_tag(message, username_)
                bot.send_message(reply, chat_)