#! /usr/bin/env python
#

import os
import glob
import json
import time

def finfo(_f):
    try:
       with open(_f, "r") as f:
          data  = json.loads(f.readline())
    except:
       data = []

    return data


files = glob.glob(os.path.expanduser("~/replays/playlist/*.fafreplay"))
files.sort()
if len(files) > 0:
    info = finfo(files[0])
    print "%s on %s (%s)" % (info["title"], info["mapname"], os.path.basename(files[0]))
else:
    print "no more replays, use !download replayid"

