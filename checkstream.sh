#!/bin/bash
# checkstream.sh
# Usage: `./checkstream.sh chinatsun` will open http://www.twitch.tv/chinatsun's stream

if [ -z "$1" ]
	then
		echo "No stream specified."
		exit 1
fi
VIEWING=$(ps aux | grep -c "[le]ivestreamer .*$1") # tips fedora
if [ "$VIEWING" = 1 ]
	then
		echo "Already watching."
		exit 1
fi

API=$(curl -is https://api.twitch.tv/kraken/streams/$1/) # Let's look at twitch.tv's API. Not yet sure if it's a good idea to have it stored in a var like that.
OFFLINE=$(echo "$API" | grep -c "\"stream\":null")
NOEXIST=$(echo "$API" | grep -c "does not exist") 
RIGHTNOW=$(date -Iminutes | sed -e 's/+[0-9]*$//g' -e 's/[:]/-/g') # Used as a filenaming scheme for archiving streams if that's what you want.
if [ "$NOEXIST" = 1 ] 
	then 
		echo "Channel does not exist."
		exit 1
fi
if [ "$OFFLINE" = 1 ]
	then
		echo "Stream offline."
		exit 1
fi
if [ "$VIEWING" = 0 ] # This if is a little pointless but hey~
	then
		killall livestreamer 2>/dev/null;
		#echo "Dumping to $1-$RIGHTNOW" # Uncomment this and the stuff on the next line in order to use this as a stream archiving tool.
		livestreamer twitch.tv/$1 medium # -o $1-$RIGHTNOW # A good idea might be to specify the path to where you want the streams to be saved to. i.e. -o /home/Cockbot/streams/$1-$RIGHTNOW
fi
