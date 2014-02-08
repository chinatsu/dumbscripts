#!/bin/bash
# checkstream.sh
# Usage: ./checkstream.sh chinatsun
# Will open http://www.twitch.tv/chinatsun's stream

# I look up the API directly instead of check online status with livestreamer as I think it's a tad faster.
OFFLINE=$(curl -is https://api.twitch.tv/kraken/streams/$1/ | grep -c "\"stream\":null")
VIEWING=$(ps aux | grep -c "[l]ivestreamer .*$1")
RIGHTNOW=$(date -Iminutes | sed -e 's/[0-9]*$//g' -e 's/[:+]//g')
if [ "$OFFLINE" = 1 ]
	then
		echo "Stream offline."
		exit 0
  # Let's not open the same stream more than once at a time.
	else if [ "$VIEWING" = 0 ]
		then
			# Comment the killall line to run multiple instances (probably useful if you wish to dump several streams)
			killall livestreamer 2>/dev/null;
			# echo "Dumping to $1-$RIGHTNOW"
			# Uncomment `-o $1-$RIGHTNOW' for saving the stream instead of open a media player.
			livestreamer twitch.tv/$1 best #-o $1-$RIGHTNOW
			exit 0
		else
			echo "Already watching."
			exit 0
		fi
fi
