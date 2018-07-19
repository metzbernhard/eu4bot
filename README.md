# EU4 IRC Bot

This little python scripts serves as IRC Bot for streaming EU4. It can gather several information from the save game (not Ironman!) and settings.txt and post them to the channel if viewers demand it. 

I suppose you might also just use it for playing, especially the Truce and AE List are actually more handy than what you get ingame (imho). 

## Setting up

First up, edit the env.env file with the necessary informations: 
* oauth='oauth:yourOauthToken (from the Bot)' get your oauth token here: https://twitchapps.com/tmi/
* bot='Username of the bot' This needs to be a valid Twitch account you can get the oauth token for
* channel='Channel you want to use it in'
* path='Path to the EU4 Documents path, the one with settings.txt in it, in python format'
* game='Path to the EU4 Game, containing eu4.exe, in python format'

The tool also supports getting all or part of its parameters via the commandline. 
`python app.py -h`

```
EU4 IRC Bot

optional arguments:
  -h, --help  show this help message and exit
  -b BOT      Twitch Account used as bot
  -c CHANNEL  Channel you want to use
  -o AUTH     oauth "oauth:oauth_token"
  -p PATH     Path to the settings.txt
  -g GAME     Path to the EU4 Game-Directory 
```


## Usage

Simply run 'python app.py' in a terminal and let it run. Currently it supports four commands:

* !ideen -> gives out the ideas from the player from latest save
* !mods -> gives out the mods from settings.txt with pretty names
* !ae -> gives out the AE (over 10) against the player (takes a few secs) 
* !waffenstillstand -> shows current Truces

As you can see the commands are a bit german, because I wrote this bot for my german Twitch-Channel. If you don't want to ask your viewers to type in this devil tounge, open the **app.py** and change the commands to whatever you want. 

If you have questions, please ask.   
If you have suggestions for better performance, more beautiful code ..., please tell me. 

Have fun! 
