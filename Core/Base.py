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

import io
import requests
import json
import configparser as cfg
import shutil
import time

from Utils import Logger as Log
from urllib.parse import quote

from Core.Error import InvalidKickTime, Unauthorized, NoQuotedMessage, UnkownError, NotEnoughtRights, BadRequest, NotFound404
from Core import Unreloaded

bans = {"h12": 43200, "h10": 36000, "h8": 28800, "h4": 14400, "h2": 7200, "h1": 3600, "h0": 1800, "ever": 0}

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

#    def send_message(self, msg, chat_id):
#        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
#        if msg is not None:
#            requests.get(url)

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

    def get_symbol(self, text):
        return "" if text .endswith("?") else "&"

    def make_request(self, method, **kwargs):
        req= self.base + method + "?"

        for key, value in kwargs.items():
            if not value:
                continue
            req += "&%s=%s" % (key, quote(str(value)))
        
        req = req.replace("?&", "?", 1)

        r = requests.get(req)

        if r.status_code != 200:
            if "rights" in r.json()["description"]:
                raise NotEnoughtRights

        if r.status_code == 403 or "Unauthorized" in r.json()["description"]:
            raise Unauthorized

        if r.status_code == 400:
            raise BadRequest(r.json()["description"] + " :(")

        if r.status_code == 404:
            raise NotFound404

        else:
            raise UnkownError(r.json()["description"])

        data = r.json()
        data["req"] = req
        del r
        return data

    def make_post(self, method, chat_id, photo=None, voice=None, document=None, certificate=None, caption=None,
                reply_to_message_id=None):
        url = self.base + method
        if chat_id:
            url += "?chat_id=" + str(chat_id)

        files = None

        if photo:
            files = {"photo": photo}

        if voice:
            files = {"voice": voice}

        if document:
            files = {"document": document}

        if certificate:
            files = {"certificate": certificate}

        if not files:
            return

        if reply_to_message_id:
            url += get_symbol(url) + "reply_to_message_id=%s" % reply_to_message_id
        if caption:
            url += get_symbol(url) + "caption=%s" % caption
        try:
            r = requests.post(url, files=files)

            if r.status_code != 200:
                if "rights" in r.json()["description"]:
                    raise NotEnoughtRights

                if r.status_code == 403:
                    raise Unauthorized

                else:
                    raise UnkownError(r.json()["description"])
            return r.json()["result"]
        except Exception as err:
            Log.e(url)
            Log.e(err)

    def kick_chat_member(self, chat_id, user_id, until=None):
        if until:
            if until not in bans:
                Log.d("Invalid kick time")
                raise InvalidKickTime(until)

            until = time.time() + bans[until]
        
        return make_request("kickChatMember", chat_id=chat_id, user_id=user_id, until_date=until)["result"]
    
    def get_chat_administrators(self, chat_id):
        return make_request("getChatAdministrators", chat_id=chat_id)["result"]

    def get_chat_member(self, chat_id, user_id):
        return make_request("getChatMember", chat_id=chat_id, user_id=user_id)

    def split_word(self, w):
        split = -((-len(w)) // 2)
        return [w[:split], w[split:]]

    def send_message(self, chat_id, text, reply_to_message_id=None, parse_mode=None, disable_web_page_preview=None, reply_markup=None):
        if len(quote(text)) > 4000:
            for part in split_word(text):
                if parse_mode:
                    if part.count("*") % 2 != 0:
                        part += "*"
                    if part.count("`") % 2 != 0:
                        part += "`"
                sendMessage(chat_id, part, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
        else:
            return make_request("sendMessage",
                                text=text,
                                chat_id=chat_id,
                                reply_to_message_id=reply_to_message_id,
                                parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview,
                                reply_markup=reply_markup)["result"]
        return

    def restrict_chat_member(self, chat_id, user_id,
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_other_messages=True,
                            can_add_web_page_previews=True):
        return make_request("restrictChatMember",
                            chat_id=chat_id,
                            user_id=user_id,
                            can_send_messages=can_send_messages,
                            can_send_media_messages=can_send_media_messages,
                            can_send_other_messages=can_send_other_messages,
                            can_add_web_page_previews=can_add_web_page_previews)["result"]
            
    def send_voice(self, chat_id, file_id, reply_to_message_id=None, caption=None):
        return make_post("sendVoice", chat_id, voice=getFile(file_id),
                     reply_to_message_id=reply_to_message_id, caption=caption)

    def send_sticker(self, chat_id, sticker=None, reply_to_message_id=None):
        make_request("sendSticker",
                 sticker=sticker,
                 chat_id=chat_id,
                 reply_to_message_id=reply_to_message_id)

    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None):
        if isinstance(photo, io.BytesIO):
            way = make_post
        else:
            way = make_request
        return way("sendPhoto",
               chat_id=chat_id,
               photo=photo,
               reply_to_message_id=reply_to_message_id,
               caption=caption)

    def send_video(self, chat_id, video, caption=None, reply_to_message_id=None):
        return make_request("sendVideo",
                        chat_id=chat_id,
                        reply_to_message_id=reply_to_message_id,
                        video=video, caption=caption)

    def send_document(self, chat_id, document, caption=None, reply_to_message_id=None):
        return make_request("sendDocument",
                        chat_id=chat_id,
                        reply_to_message_id=reply_to_message_id,
                        document=document,
                        caption=caption)
        
    def send_file_document(self, chat_id, document_path, caption=None, reply_to_message_id=None):
        return make_post("sendDocument",
                     chat_id=chat_id,
                     reply_to_message_id=reply_to_message_id,
                     document=open(document_path),
                     caption=caption)

    def send_photo_file(self, chat_id, photo, caption=None, reply_to=None):
        return make_post("sendPhoto", chat_id=chat_id, photo=photo,
                     caption=caption, reply_to_message_id=reply_to)

    def send_chat_action(self, chat_id, action): return make_request("sendChatAction", chat_id=chat_id, action=action)

    def get_file_name(self, file_id):
        return make_request("getFile", file_id=file_id)["result"]["file_path"].split("/")[1]

    def get_file(self, file_id, out=None, file_path=None):
        if not out:
            out = io.BytesIO()
        if not file_path:
            file_path = make_request("getFile", file_id=file_id)["result"]["file_path"]
        x = requests.get(self.base + "%s" % (file_path), stream=True)  # .json()["result"]
        if x.status_code == 200:
            x.raw.decode_content = True
            shutil.copyfileobj(x.raw, out)
        else:
            Log.w("Invalid status code %s" % x.status_code)
            return None
        del x
        out.seek(0)
        return out

    def unban_chat_member(self, chat_id, user_id):
        return make_request("unbanChatMember", chat_id=chat_id, user_id=user_id)
    
    def get_me(self):
        bot = make_request("getMe")
        if not bot:
            return None
        bot = bot["result"]
        
        bot["token"] = self.token
        return bot

    def get_chat(self, chat_id):
        return make_request("getChat", chat_id=chat_id)

    def edit_message_text(self, chat_id=None, message_id=None, text=None, parse_mode=None):
        return make_request("editMessageText", chat_id=chat_id,
                        message_id=message_id, text=text, parse_mode=parse_mode)

    def delete_message(self, chat_id=None, message_id=None):
        return make_request("deleteMessage", chat_id=chat_id, message_id=message_id)


    deleteMessage = delete_message
    editMessageText = edit_message_text
    getUpdates = get_updates
    #deleteWebhook = delete_webhook
    #setWebhook = set_webhook
    getChat = get_chat
    getMe = get_me
    unbanChatMember = unban_chat_member
    getFile = get_file
    getFileName = get_file_name
    sendChatAction = send_chat_action
    sendPhotoFile = send_photo_file
    sendFileDocument = send_file_document
    sendDocument = send_document
    sendVide = send_video
    sendPhoto = send_photo
    sendSticker = send_sticker
    sendVoice = send_voice
    sendVideo = send_video
    #leaveChat = leave_chat
    restrictChatMember = restrict_chat_member
    sendMessage = send_message
    getChatMember = get_chat_member
    getChatAdministrators = get_chat_administrators
    #setChatPhoto = set_chat_photo
    #setChatDescription = set_chat_description
    #setChatTitle = set_chat_title
    #getInviteLink = get_invite_link
    #unpinMessage = unpin_message
    #pinMessage = pin_message
    kickChatMember = kick_chat_member
    #getChatPhoto = get_chat_photo
    #getUserPhoto = get_user_photo