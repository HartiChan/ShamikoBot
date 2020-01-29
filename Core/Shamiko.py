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


import requests
import json
import configparser as cfg

class telegram_chatbot():
    def __init__(self, config):
        self.token = self.ReadTokenFromConfig(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
        self.masterID = self.ReadMasterID(config)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def sendbootmsg(self, bootmsg):
        url = self.base + "sendMessage?chat_id={}&text={}".format(self.masterID, bootmsg)
        requests.get(url)

    def ReadTokenFromConfig(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
    
    def ReadMasterID(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'masterID')
