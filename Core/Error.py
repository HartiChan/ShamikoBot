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


class KitsuError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class InvalidKickTime(KitsuError):
    def __init__(self, until):
        super(InvalidKickTime, self).__init__('%s it is not valid as kicktime' % until)


class Unauthorized(KitsuError):
    def __init__(self):
        self.message = "Not allowed."


class NoQuotedMessage(KitsuError):
    def __init__(self):
        self.message = "No messages have been quoted."


class UnkownError(KitsuError):
    def __init__(self, value):
        self.message = "Unknown error: %s" % value


class NotOkError(KitsuError):
    def __init__(self, value):
        self.message = "Request not ok: %s" % value


class NotEnoughtRights(KitsuError):
    def __init__(self):
        self.message = "The bot doesn't have enough permissions."


class GeneralError(KitsuError):
    def __init__(self, desc):
        self.message = "Generic error: %s" % desc


class BadRequest(KitsuError):
    def __init__(self, desc):
        self.message = "%s" % desc


class NotFound404(KitsuError):
    def __init__(self):
        self.message = "The requested resource was not found."


class ServerError(Exception):
    def __init__(self, message):
        super(ServerError, self).__init__()
        self.message = message

    def __str__(self):
        return '%s' % self.message


class TelegramError(Exception):
    def __init__(self, message):
        super(TelegramError, self).__init__()
        self.message = message

    def __str__(self):
        return '%s' % self.message