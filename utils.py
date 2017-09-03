import config
import urllib.request
import json
from time import sleep

def msg(sock, message):
    sock.send("PRIVMSG #{} :{} \r\n".format(config.CHAN, message).encode("utf-8"))
    print("PRIVMSG #{} :{} \r\n".format(config.CHAN, message).encode("utf-8"))

def ban(sock, user):
    msg(sock, ".ban {}".format(user))

def timeout(sock, user, seconds = 300):
    msg(sock, ".timeout {} {}".format(user, seconds))

#def pm(sock, user, mess):
#    sock.send("PRIVMSG {} :{} \r\n".format(user, mess).encode("utf-8"))

#http://tmi.twitch.tv/group/user/excorex/chatters
def fillUpOps():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/excorex/chatters"
            req = urllib.request.Request(url)
            req.add_header("accept", "*/*")
            res = urllib.request.urlopen(req).read().decode("utf-8")
            if res.find("502 bad gateway") == -1:
                config.oplist.clear()
                data = json.loads(res)
                for e in data["chatters"]["moderators"]:
                    config.oplist[e] = "mod"
                for e in data["chatters"]["staff"]:
                    config.oplist[e] = "staff"
                for e in data["chatters"]["admins"]:
                    config.oplist[e] = "admin"
                for e in data["chatters"]["global_mods"]:
                    config.oplist[e] = "global_mod"
        except:
            "Error"
        sleep(5)

def isOp(user):
    return user in config.oplist