#! /usr/bin/env python
#

import irc.bot
import irc.strings
import os
import glob
import json
import time
import urllib
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

with open(os.path.expanduser('~/.twitch_irc_key'), 'r') as f:
    IRC_KEY = f.read().replace('\n' , '')

class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self):
        irc.bot.SingleServerIRCBot.__init__(self, [("irc.twitch.tv", 6667, IRC_KEY)], "faf_test_account", "justabot")
    	self.chan = "#faf_test_account"
        self.lasttime = time.time()

    def on_welcome(self, c, e):
        c.join(self.chan)

    def on_pubmsg(self, c, e):
        message = e.arguments[0]
        if len(message) <= 1 or message[0] != "!" or time.time() - self.lasttime < 5:
            return
    
        cmd = message[1:]
        nick = e.source

        if cmd == "now":
            files = glob.glob(os.path.expanduser('~/replays/playlist/*.fafreplay'))
            files.sort()
            if len(files) > 0:
                info = self.info(files[0])
                c.privmsg(self.chan, "now playing: %s on %s (%s)" % (info["title"], info["mapname"], os.path.basename(files[0])))
        elif cmd == "remaining":
            files = glob.glob(os.path.expanduser('~/replays/playlist/*.fafreplay'))
            c.privmsg(self.chan, "replays in que: %d" % (len(files) - 1))
        elif cmd == "next":
            files = glob.glob(os.path.expanduser('~/replays/playlist/*.fafreplay'))
            files.sort()
            if len(files) > 1:
                info = self.info(files[1])
                c.privmsg(self.chan, "next replay: %s on %s (%s)" % (info["title"], info["mapname"], os.path.basename(files[0])))
            else:
                c.privmsg(self.chan, "no more replays")
        elif len(cmd.split(" ")) == 2 and cmd.split(" ")[0] == "download" and cmd.split(" ")[1].isdigit():
            replayid = cmd.split(" ")[1]
            baseurl = "http://content.faforever.com/faf/vault/replay_vault/replay.php?id="
            urllib.urlretrieve(baseurl + replayid, os.path.expanduser("~/replays/playlist/" + replayid + ".fafreplay"))
            c.privmsg(self.chan, "replay %s added to playlist" % (replayid))
        elif cmd == "faster":
            os.system('xvkbd -text "\[0xFFAB]"')
            c.privmsg(self.chan, "gamesped +1")
        elif cmd == "slower":
            os.system('xvkbd -text "\[0xFFAD]"')
            c.privmsg(self.chan, "gamespeed -1")
        elif cmd == "showfps":
            c.privmsg(self.chan, "fps counter toggled")
            os.system('xvkbd -text "\[0xFFAF]"')

        self.lasttime = time.time()
         
    def info(self, _f):
        try:
            with open(_f, "r") as f:
                data  = json.loads(f.readline())
        except:
            data = []

        return data

if __name__ == "__main__":
    os.environ["DISPLAY"] = ":0"
    Bot().start()

