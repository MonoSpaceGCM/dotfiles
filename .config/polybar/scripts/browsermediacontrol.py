#!/usr/bin/python3
import sys
import os
import argparse
from pydbus import SessionBus
from gi.repository import GLib
#import sys
#import os
#import argparse

ICON_PLAY = "\u25B6 "
ICON_PAUSE = "\u23F8 "
ICON_NEXT = "c"#"\uf152"
ICON_PREV = "d"#"\uf191"
ICON = ""
PATH=os.path.realpath(__file__)
TITLE_LENGTH = 80

parser = argparse.ArgumentParser()
parser.add_argument('--volume', type=int)
parser.add_argument('--playpause', action="store_true")
parser.add_argument('--next', action="store_true")
parser.add_argument('--prev', action="store_true")
args= parser.parse_args()

bus = SessionBus()
try:
    Player = bus.get(
        "org.kde.plasma.browser_integration",
        "/org/mpris/MediaPlayer2"
    )
except GLib.Error:
    sys.exit()

def action(command, text):
    #return "%{A1:" + PATH + " --" + command + ":}" + text + "%{A}"
    return text + "%{A}"

def truncate(text, max_len):
    return text[:max_len] + "..." if len(text) > max_len and max_len > 0 else text

if Player.PlaybackStatus != "Stopped":
    if args.volume is not None:
        vol = Player.Volume
        Player.Volume = vol + (args.volume * 0.1)
        sys.exit()
    if args.playpause:
        Player.PlayPause()
        sys.exit()
    if Player.PlaybackStatus=="Playing":
        ICON = ICON_PAUSE
    elif Player.PlaybackStatus=="Paused":
        ICON = ICON_PLAY
    if args.next:
        Player.Next()
    elif args.prev:
        Player.Previous()
    title = Player.Metadata["xesam:title"]
    output = ICON + truncate(title, TITLE_LENGTH)
    print(output)
else:
    print("")
