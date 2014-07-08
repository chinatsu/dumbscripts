dumbscripts
===========

Scripts for various purposes.

##srl.sh
A simple script that looks up the http://speedrunslive.com API and outputs the top `n` streamers currently streaming. `n` equals to 10 if no number is specified. For example, `srl.sh 40` will output the top 40 streamers, or as many as there are if there are less than 40 people currently streaming.

##checkstream.sh
A script that checks the http://twitch.tv API if a specified stream is online. Once the API successfully goes through some checks (if the stream is already open, if it's offline/banned, etc.), it will spawn a livestreamer instance. I did it this way for the sake of a cronjob scenario. Since livestreamer has the option to output the stream into a file, one can easily use it for archiving streams for watching later.

##thread.php
A quick redirect script to find the speedrunning general thread on /vg/. The regex should in 99% of cases work just fine, but it hasn't really been tested extensively yet. I wanted to have a bookmark of sorts to quickly get to the thread, instead of using .thread in the IRC channel, or wade through the catalog.

##shitradio.py
A little PyQT applet for listening to radio, it has almost no use, no comments and no sanity.
