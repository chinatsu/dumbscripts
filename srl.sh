#!/bin/bash
# Depends on
# jshon (http://kmkeen.com/jshon)
# livestreamer (https://github.com/chrippa/livestreamer)
# curl (http://curl.haxx.se)
case $1 in
[!0-9]*) echo -e "Argument \033[32m$1 \033[0mis not a number."; exit 1 ;;
'') a=10;;
*) a=$1;;
esac
echo "Top $a streamers:"
curl -s http://api.speedrunslive.com/test/team > .tempapi
jshon -e channels -a -e channel -e display_name -u -p -e meta_game -u < .tempapi |
awk '{printf("%s",NR%2 ? $0"\t":$0"\n")}' | # this awk line gives me the opportunity to add more stuff from the API easily, but for now I'd rather keep it short and sweet
head -n "$a" |
sed -e "s/&#39;/\'/" -e 's/\t/ is playing: "/' -e 's/$/"/' -e 's/Super Mario /SM/' -e 's/The Legend of Zelda: //' -e 's/Grand Theft Auto/GTA/' | # Starting from the 4th -e argument are personal preferences, mostly to save space.
cat -n
echo -e '\nInput a\033[32m number \033[0mto select a stream.'
read num
case $num in
[!0-9]*) echo "That's not a number, exiting."; exit 1; rm -f .tempapi ;;
*) numfix=$((num - 1))
name=$(jshon -e channels -e $numfix -e channel -e name -u < .tempapi)
viewers=$(jshon -e channels -e $numfix -e channel -e current_viewers -u < .tempapi)
title=$(jshon -e channels -e $numfix -e channel -e title -u < .tempapi)
rm -f .tempapi
echo -e "\nCurrent viewers: \033[032m$viewers\n\033[0mTitle: \033[032m$title\n\033[0m"
livestreamer http://twitch.tv/"$name" best
exit 1 ;;
esac
