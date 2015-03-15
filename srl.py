#!/usr/bin/env python3
import requests
import subprocess
import os
import argparse
from html import parser

#TODO
# Some browsing functionality

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
               'oot': 'ocarina of time',
               'tww': 'the wind waker',
               'sm': 'super metroid',
               'tes': 'elder scrolls',
               'das': 'dark souls',
               'dk': 'donkey kong',
               'ff': 'final fantasy'
               }

parser = argparse.ArgumentParser()
parser.add_argument('--game', help='Displays streams with matching string in games', nargs='?', default=None)
args = parser.parse_args()
if args.game:
    for alias in gameAliases:
        if args.game == alias:
            gSearch = gameAliases[alias]
            break
    else:
        gSearch = args.game
else:
    gSearch = None

def getApi():
    try:
        streamJson = requests.get('http://api.speedrunslive.com/frontend/streams', timeout=10).json()
        return streamJson
    except:
        return None

def populateList(apiResponse, search):
    printList = []
    if apiResponse != None:
        for channel in apiResponse['_source']['channels']:
            game = h.unescape(channel['meta_game'])
            title = h.unescape(channel['title'])
            if channel['api'] == 'twitch':
                url = 'http://twitch.tv/' + channel['name']
            elif channel['api'] == 'hitbox':
                url = 'http://hitbox.tv/' + channel['name']
            name = channel['display_name']
            viewers = channel['current_viewers']
            if search == None or search.lower() in game.lower():
                printList.append({'game': game, 'title': title, 'url': url, 'name': name, 'viewers': viewers})
            else:
                pass
            finalList = sorted(printList, key=lambda k: k['viewers'], reverse=True)
        return finalList

    else:
        return None


def termDisplay(pList, tHeight):
    if len(pList) < tHeight:
        listLength = len(pList)
    else:
        listLength = tHeight
    for channel in range(0,listLength):
        print(str(int(channel) + 1) + ': \033[037m' + pList[channel]['name'] +
              '\033[0m -- '+ pList[channel]['game'] + '\n\t\033[036m' +
              pList[channel]['title'] + '\033[0m -- Viewers: ' + str(pList[channel]['viewers']))
    return listLength
    
pList = populateList(getApi(), gSearch)
if len(pList) == 0:
    print('No streams to display')
elif pList != None:
    listLength = termDisplay(pList, tHeight)
    streamSelect = input('Select stream to watch [1-' + str(listLength) + ']: ')
    try:
        streamInt = int(streamSelect)
        if streamInt > listLength:
            print('Selected stream out of range')
        elif streamInt == 0:
            print('Selected stream out of range')
        else:
            selectedStream = pList[streamInt - 1]
            print(selectedStream['url'])
            # really not a nice way to open livestreamer but who cares
            subprocess.Popen(['livestreamer', selectedStream['url'], livestreamerQuality])
    except ValueError:
        print('Input is not a number')
