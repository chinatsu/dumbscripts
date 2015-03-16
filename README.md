dumbscripts
===========

Scripts for various purposes.

##srl.py
A simple script that looks up the http://speedrunslive.com API and outputs the top `n` streamers. `n` is determined by your tty's height.

###Flags
* `-g term`, `--game term`: Filters output based on game. Usage: `srl.py -g lttp` - only displays A Link To The Past streams. Equals `srl.py -g 'a link to the past'`. View the few search aliases near the top of the script.
* `-s int`, `--streams int`: Displays int amount of streams instead of the default based on tty height.
* `-r int-int`, `--range int-int`: Displays streams within the set range of viewers. Usage: `srl.py -r 0-10` - only displays streams with 0 to 10 viewers.
* `--race y/n`: Displays streams currently in a race. Useful along with the `-g` flag. Usage: `srl.py --race y` - only displays streams in a race. `--race n` will only show streams not in a race.
* `--reverse`: Reverses list based on viewer count.


##checkstream.sh
A script that checks the http://twitch.tv API if a specified stream is online. Once the API successfully goes through some checks (if the stream is already open, if it's offline/banned, etc.), it will spawn a livestreamer instance. I did it this way for the sake of a cronjob scenario. Since livestreamer has the option to output the stream into a file, one can easily use it for archiving streams for watching later.

##thread.php
A quick redirect script to find the speedrunning general thread on /vg/. The regex should in 99% of cases work just fine, but it hasn't really been tested extensively yet. I wanted to have a bookmark of sorts to quickly get to the thread, instead of using .thread in the IRC channel, or wade through the catalog.

##shitradio.py
A little PyQT applet for listening to radio, it has almost no use, no comments and no sanity.
