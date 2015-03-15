#!/bin/bash
# checkstream.sh
# Usage: `./checkstream.sh chinatsun` will open http://www.twitch.tv/chinatsun's stream
# Someone asked me if livestreamer could be used as a cronjob for archiving livestreams from twitch, but I feel like that might be a little clunky. I decided to write something simple that wouldn't spawn livestreamer until it really knows that it's necessary.

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

API=$(curl -is https://api.twitch.tv/kraken/streams/"$1"/) # Let's look at twitch.tv's API. Not yet sure if it's a good idea to have it stored in a var like that.

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

# You can probably uncomment this if you want to run multiple instances at once, i.e. archiving multiple streams or whatever. I haven't tried myself, though.
killall livestreamer 2>/dev/null;

# Uncomment for archiving streams.
#RIGHTNOW=$(date -Iminutes | sed -e 's/+[0-9]*$//g' -e 's/[:]/-/g'); echo "Dumping to $1-$RIGHTNOW"; livestreamer twitch.tv/"$1" best -o $1-$RIGHTNOW;

# Also consider commenting this if you're going to use the line above.
livestreamer twitch.tv/"$1" medium
