# log-reader
this repo is a simple .log file reader for omega strikers.
omega strikers is built with unreal engine 5. there's a debugger for it that the devs use. basically as you play a game of omega strikers, there are debugging messages that get saved locally. we can access those messages in real time! the messages are save in a .log file, typically it's 'OmegaStriker.log'. the devs often request log files from people submitting bug reports.

this repo is meant to be a relatively simple example, missing some features like checking if the game omega strikers is already open.


## setup:
install this library.

> pip install watchdog
> pip install PyGetWindow


download main.py somewhere on your PC.


## how to run this

have the game omega strikers open (do this first).
then run 'python main.py'(do this second).

if you click around in omega strikers (ex go to your settings, go to the shop, play a game), you will generate logs. if logs are generated, they are detected and printed! I recommend setting up some kind of whitelist or blacklist of words.

"self.file_size = 0" gets initialized to 0 but it doesn't get reset. which is why i check to see if omega strikers is running before letting the observer start observing, and ends the observer if it notices that the game is trying to shut down. (you can circumvent/delete this just be prepared to rewrite code it's just how I did things.)


