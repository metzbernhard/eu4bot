# EU4 IRC Bot for JakeChat

Special version of my EU4 Chat bot, that uses whispers for Jakechat.
Times out people that try to use botcommands in chat and tells them to use whispers. 

## Setting up

Download code as zip-package and extract.

First up, edit the config.json file with the necessary informations:
* oauth='oauth:yourOauthToken (from the Bot)' get your oauth token here: https://twitchapps.com/tmi/
* bot='Username of the bot' This needs to be a valid Twitch account you can get the oauth token for
* channel='Channel you want to use it in'
* path='Path to the EU4 Documents path, the one with settings.txt in it, either with \\ or /'
* game='Path to the EU4 Game, containing eu4.exe, either with \\ or /'
* language='english or german'
* ironman='True or False' set this to True for ironman or use the -i flag, otherwise the bot commands will fail

The tool also supports getting all or part of its parameters via the commandline. The ones you don't provide in the command line, it'll try to retreive from the *config.json* file. If you for example don't want your oauth-token to be in the file as plain text you could add all informations but the oauth-token in the *config.json* file and call the app via `python app.py -o oauth:oauthtokenhere`

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
  -l LANGUAGE  english or german
  -i           ironman-flag

```


## Usage

Simply run 'python app.py' in a terminal and let it run. Currently it supports four commands:

* ideas -> shows ideas
* mods -> gives out the mods from settings.txt with pretty names
* ae -> gives out the AE (over 10) against the player (takes a few secs)
* truces -> shows current Truces
* commands -> shows commands
* uptime -> shows uptime

If you have questions, please ask.   
If you have suggestions for better performance, more beautiful code ..., please tell me.

Have fun!

![example](https://github.com/metzbernhard/eu4bot/blob/master/ae.png)
![example](https://github.com/metzbernhard/eu4bot/blob/master/commands.png)
![example](https://github.com/metzbernhard/eu4bot/blob/master/ideas.png)
![example](https://github.com/metzbernhard/eu4bot/blob/master/mods.png)
![example](https://github.com/metzbernhard/eu4bot/blob/master/truces.png)
![example](https://github.com/metzbernhard/eu4bot/blob/master/uptime.png)
