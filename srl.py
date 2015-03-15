#!/usr/bin/env python3
import requests
import subprocess
import os
from html import parser

# config
livestreamerQuality = 'medium, source'

# not config
tHeight = int((int(os.popen('stty size', 'r').read().split()[0]) - 4) / 2)
h = parser.HTMLParser()

def getApi():
    try:
        streamJson = requests.get('http://api.speedrunslive.com/frontend/streams', timeout=10).json()
        return streamJson
    except:
        return None

def populateList(apiResponse):
    if apiResponse != None:
        printList = []
        for channel in apiResponse['_source']['channels']:
            game = h.unescape(channel['meta_game'])
            title = h.unescape(channel['title'])
            if channel['api'] == 'twitch':
                url = 'http://twitch.tv/' + channel['name']
            elif channel['api'] == 'hitbox':
                url = 'http://hitbox.tv/' + channel['name']
            name = channel['display_name']
            viewers = channel['current_viewers']
            printList.append({'game': game, 'title': title, 'url': url, 'name': name, 'viewers': viewers})
            finalList = sorted(printList, key=lambda k: k['viewers'], reverse=True)
        return finalList
    else:
        return None


def termDisplay(pList, tHeight):
    for channel in range(0,tHeight):
        print(str(int(channel) + 1) + ': \033[037m' + pList[channel]['name'] +
              '\033[0m -- '+ pList[channel]['game'] + '\n\t\033[036m' +
              pList[channel]['title'] + '\033[0m -- Viewers: ' + str(pList[channel]['viewers']))
    
pList = populateList(getApi())
if pList != None:
    termDisplay(pList, tHeight)
    streamSelect = input('Select stream to watch [1-' + str(tHeight) + ']: ')
    try:
        streamInt = int(streamSelect)
        if streamInt > tHeight:
            print('Selected stream out of range')
        elif streamInt == 0:
            print('Selected stream out of range')
        else:
            selectedStream = pList[streamInt - 1]
            print(selectedStream['url'])
            subprocess.Popen(['livestreamer', selectedStream['url'], livestreamerQuality])
    except ValueError:
        print('Input is not a number')
