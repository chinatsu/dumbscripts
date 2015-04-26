#!/usr/bin/env python3
import requests
import subprocess
import os
import argparse
import sys
from html import parser

#TODO
# Some (more) ways to refine output?

# config
livestreamerQuality = 'medium, source'

# not config
tHeight = int((int(os.popen('stty size', 'r').read().split()[0]) - 4) / 2)
h = parser.HTMLParser()
gameAliases = {
               'gta': 'grand theft auto',
               'sm64': 'super mario 64',
               'sms': 'super mario sunshine',
               'alttp': 'a link to the past',
               'lttp': 'a link to the past',
               'oot': 'ocarina of time',
               'tww': 'the wind waker',
               'sm': 'super metroid',
               'tes': 'elder scrolls',
               'das': 'dark souls',
               'dk': 'donkey kong',
               'ff': 'final fantasy',
               'smb': 'super mario bros',
               'tyd': 'thousand year door'
               }

cli = argparse.ArgumentParser()
tError = '\033[032mError: \033[0m'
tWarning = '\033[036mWarning: \033[0m'
cli.add_argument('--game', '-g',
                    help='Displays streams with matching string in games',
                    nargs='?', metavar='search', default=None)
cli.add_argument('--race',
                    help='Displays streams currently in a race',
                    nargs='?', metavar='y/n', default=None)
cli.add_argument('--range', '-r',
                    help='Display streams within the specified range of viewers',
                    nargs='?', metavar='min-max', default=None)
cli.add_argument('--streams', '-s',
                    help='Display amount of streams',
                    nargs='?', metavar='n', type=int, default=None)
cli.add_argument('--reverse',
                    help='Sort streams by least to most viewers',
                    action='store_true', default=False)
cli.add_argument('--quality', '-q',
                    help='Sets livestreamer quality. Default: \'medium, source\'',
                    nargs='?', metavar='quality', default=livestreamerQuality)

args = cli.parse_args()

if args.race:
    if args.race.lower() in ['yes', 'y', 'true', '1']:
        args.race = True
    elif args.race.lower() in ['no', 'n', 'false', '0']:
        args.race = False
    else:
        print(tWarning + '\'' + args.race + '\' is not a valid boolean value. Defaulting to None')
        args.race = None

if args.range:
    view_range = args.range.split('-')
    try:
        if int(view_range[1]) < int(view_range[0]):
            maxRange = int(view_range[0])
            minRange = int(view_range[1])
        else:
            maxRange = int(view_range[1])
            minRange = int(view_range[0])
    except:
        print(tError + 'Not a valid range.\nUsage example: srl.py --view-range 3-7')
        sys.exit()

if args.game:
    for alias in gameAliases:
        if args.game == alias:
            args.game = gameAliases[alias]
            break

if args.streams != None:
    if args.streams == 0:
        print(tWarning + 'Defaulting to ' + str(tHeight) + ' streams.')
    else:    
        tHeight = args.streams


def getApi():
    try:
        streamJson = requests.get('http://api.speedrunslive.com/frontend/streams', timeout=10).json()
        return streamJson
    except:
        return None

def populateList(apiResponse, args):
    printList = []
    if apiResponse != None:
        for channel in apiResponse['_source']['channels']:
            game = h.unescape(channel['meta_game'])
            title = h.unescape(channel['title'])
            if channel['is_racing'] == 1:
                is_racing = True
            elif channel['is_racing'] == 0:
                is_racing = False
            if channel['api'] == 'twitch':
                url = 'http://twitch.tv/' + channel['name']
            elif channel['api'] == 'hitbox':
                url = 'http://hitbox.tv/' + channel['name']
            name = channel['display_name']
            viewers = int(channel['current_viewers'])
            if args.game == None or args.game.lower() in game.lower():
                if args.race == is_racing or args.race == None:
                    if (args.range and maxRange >= viewers >= minRange) or not args.range:
                        printList.append({'game': game, 'title': title, 'url': url, 'name': name, 'viewers': viewers})
            else:
                pass
            if args.reverse:
                finalList = sorted(printList, key=lambda k: k['viewers'])
            else:
                finalList = sorted(printList, key=lambda k: k['viewers'], reverse=True)
        return finalList

    else:
        return None


def termDisplay(pList, tHeight):
    if pList and len(pList) < tHeight:
        listLength = len(pList)
    else:
        listLength = tHeight
    for channel in range(0,listLength):
        print(str(int(channel) + 1) + ': \033[032m' + pList[channel]['name'] +
              '\033[0m -- '+ pList[channel]['game'] + '\n\t\033[033m' +
              pList[channel]['title'] + '\033[0m -- Viewers: ' + str(pList[channel]['viewers']))
    return listLength
    
pList = populateList(getApi(), args)
if not pList or len(pList) == 0:
    print(tError + 'No streams to display')
elif pList != None:
    listLength = termDisplay(pList, tHeight)
    streamSelect = input('Select stream to watch [\033[034m1-' + str(listLength) + '\033[0m]: ')
    try:
        streamInt = int(streamSelect)
        if streamInt > listLength or streamInt == 0:
            print(tError + 'Selected stream out of range')
        else:
            selectedStream = pList[streamInt - 1]
            # really not a nice way to open livestreamer but who cares
            subprocess.Popen(['livestreamer', selectedStream['url'], args.quality])
    except ValueError:
        print(tError + 'Input is not a number')
