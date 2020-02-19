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


import json
import os
import threading
import time

from Utils import Logger as Log, Utils
import psutil

from Core import Base

class MWT(object):
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2):
        self.timeout = timeout

    def collect(self):
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache

    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = sorted(kwargs.items())
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                v = self.cache[key] = f(*args, **kwargs), time.time()
            return v[0]

        func.func_name = f.__name__

        return func

delete_codes = {}
antisp = {}
scores = {}
gbots = {}

p = psutil.Process(os.getpid())


def blacklista(uid):
    blacklist = json.loads(open("Files/jsons/blacklist.json").read())
    blacklist.append(uid)
    with open("Files/jsons/blacklist.json", "w") as fl:
        fl.write(json.dumps(blacklist))


def remover(uid, entity):
    time.sleep(Utils.get_antispam_time(entity))
    antisp[entity].remove(uid)


def antispam(infos):
    entity = str(infos.entity)
    if entity not in antisp:
        antisp[entity] = []

    if infos.user.uid in antisp[entity]:

        if infos.user.uid not in scores:
            scores[infos.user.uid] = 0

        scores[infos.user.uid] += 1

        Log.w("%s <- %s -> [spam %s]" % (infos.bid, infos.user.uid, scores[infos.user.uid]))

        if scores[infos.user.uid] == 30:
            blacklista(infos.user.uid)
            infos.reply("User ID %s blacklisted." % infos.user.uid)
            Log.w("User ID %s blacklisted." % infos.user.uid)

        return True
    else:
        antisp[entity].append(infos.user.uid)
        threading.Thread(target=remover, args=(infos.user.uid, entity)).start()
        return False


@MWT(timeout=240)
def get_admin_ids(chat_id):
    return [admin for admin in Base.getChatAdministrators(chat_id)]


def get_cpu():
    return p.cpu_percent()


def get_memory():
    return int(p.memory_info()[0] / float(2 ** 20))


def get_time():
    return p.create_time()


def get_system_memory():
    mem = psutil.virtual_memory()
    return (mem[0] - mem[1]) >> 20


def set_delete_code(uid, code):
    delete_codes[str(uid)] = str(code)
    return True


def get_delete_code(uid):
    if str(uid) in delete_codes:
        return delete_codes[str(uid)]
    else:
        return ""