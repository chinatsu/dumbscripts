#!/bin/bash
# checkstream.sh
# Usage: `./checkstream.sh chinatsun` will open http://www.twitch.tv/chinatsun's stream

if [ -z "$1" ]
	then
		echo "No stream specified."
		exit 1
fi
if ( ps aux | grep -q "[le]ivestreamer .*$1" ) # tips fedora
	then
		echo "Already watching."
		exit 1
fi

API=$(curl -is https://api.twitch.tv/kraken/streams/$1/) # Let's look at twitch.tv's API. Not yet sure if it's a good idea to have it stored in a var like that.
RIGHTNOW=$(date -Iminutes | sed -e 's/+[0-9]*$//g' -e 's/[:]/-/g') # Used as a filenaming scheme for archiving streams if that's what you want.

if ( echo "$API" | grep -q "does not exist" )
	then 
		echo "Channel does not exist."
		exit 1
fi
if ( echo "$API" | grep -q "is unavailable" )
	then
		echo "Channel is unavailable. This usually means it's been banned. ;_;7"
		exit 1
fi
if ( echo "$API" | grep -q "is not available on Twitch" )
	then
		echo "Channel is not available on Twitch. This means it's a Justin.tv-exclusive channel."
		exit 1
fi
if ( echo "$API" | grep -q "\"stream\":null" )
	then
		echo "Stream offline."
		exit 1
fi

killall livestreamer 2>/dev/null;
#echo "Dumping to $1-$RIGHTNOW" # Uncomment this and the stuff on the next line in order to use this as a stream archiving tool.
livestreamer twitch.tv/$1 medium # -o $1-$RIGHTNOW # A good idea might be to specify the path to where you want the streams to be saved to. i.e. -o /home/Cockbot/streams/$1-$RIGHTNOW
