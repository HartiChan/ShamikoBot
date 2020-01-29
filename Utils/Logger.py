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

import time
import inspect

def lt():
    return time.strftime("%H:%M:%S")

def call_elab(caller_foo):
    return caller_foo + (14 - len(caller_foo)) * " "


def printf(type, lmsg, foo):
    text = "[ %s ] %s - [from: %s] - %s" % (type, lt(), foo, lmsg)
    with open("Files/logging.txt", "a") as fl:
        fl.write(text + "\n")
    print(text)
    return True


def printe(text):
    with open("Files/errors.txt", "a") as fl:
        fl.write(text + "\n")
        fl.close()
    print(text)


def d(text):
    printf("Debug ", text, call_elab(inspect.stack()[1][3]))


def i(text):
    printf("Info  ", text, call_elab(inspect.stack()[1][3]))


def a(text):
    printf("Action", text, call_elab(inspect.stack()[1][3]))


def w(text):
    printf("Warn  ", text, call_elab(inspect.stack()[1][3]))


def e(text):
    text = str(text)
    printe("[ Error  ] %s - [from: %s] - Errore: %s line: ~%s" % (lt(), call_elab(inspect.stack()[1][3]), text,
                                                                  inspect.getframeinfo(inspect.stack()[1][0]).lineno))
    return False


def critical(text, shutdown=True):
    text = str(text)
    printe("[CRITICAL] %s - [from: %s] - Errore critico: %s line: ~%s" % (lt(), call_elab(inspect.stack()[1][3]), text,
                                                                          inspect.getframeinfo(
                                                                              inspect.stack()[1][0]).lineno))
    if shutdown:
        exit()
