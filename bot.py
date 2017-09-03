import utils
import config
import time
import json
import urllib.request
from time import sleep
import _thread
import re
import socket

DEBUG_MODE = False

def main():
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))
    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    utils.msg(s, "Daddy here!")

    _thread.start_new_thread(utils.fillUpOps, ())

    count = 0
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.com\r\n":
            s.send("POND :tmi.twitch.com\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_message.sub("", response)
            print(response)
            #print(message.strip() == "!timeout excorex 30")
            if message.strip() == "!time":
                utils.msg(s, "It's currently " + time.strftime("%I:%M %p %Z on %A %B %d %Y"))

            if message.strip() == "!oplist":
                utils.msg(s, "Op list: ")
                for e in config.oplist:
                    utils.msg(s, "{}: {}".format(e, config.oplist[e]))

            if message.strip() == "!promote":
                utils.msg(s, "Dota = говно")
                utils.msg(s, "eXCore = царь")

            if re.fullmatch(r"!to \w+ \d+", message.strip()) and utils.isOp(username):
                name = re.search(r" (\w+) ", message.strip()).group(1)
                totime = re.search(r" (\d+)$", message.strip()).group(1)
                utils.timeout(s, name, totime)
                utils.msg(s, name + " is timeouted for " + totime + " seconds")

            if message.strip() == "!chatters":
                url = "http://tmi.twitch.tv/group/user/excorex/chatters"
                req = urllib.request.Request(url)
                req.add_header("accept", "*/*")
                res = urllib.request.urlopen(req).read().decode("utf-8")
                if res.find("502 bad gateway") == -1:
                    data = json.loads(res)
                    for e in data["chatters"]:
                        for c in data["chatters"][e]:
                            mas = "{} : {}".format(c, e)
                            utils.msg(s, mas[:-1])
                    utils.msg(s, "Total chatters: {}".format(data["chatter_count"]))
            #if re.fullmatch(r"^!sendpm \w+ .*", message.strip()):                 ##Not Working
            #    name = re.search(r"!sendpm (\w+) ", message.strip()).group(1)
            #    mess = re.search(r"!sendpm \w+ (.*)", message.strip()).group(1)
            #    utils.pm(s, name, mess)
        count+=1
        if DEBUG_MODE and count > 1:
            cmd = input()
            s.send(cmd.encode("utf-8"))
        sleep(1)
if __name__ == "__main__":
    main()
