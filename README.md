# EU4 IRC Bot

This little python scripts serves as IRC Bot for streaming EU4. It can gather several information from the save game (not Ironman!) and settings.txt and post them to the channel if viewers demand it. 

I suppose you might also just use it for playing, especially the Truce and AE List are actually more handy than what you get ingame (imho). 

This sadly does not work with **Ironman** files, since their information is not plainly extractable. Just don't stream with Ironman, it's useless anyway, it prevents neither cheating (lookup exploits and cheatengine) nor savescumming (lookup birding). You know what prevents cheating & savescumming? Having people watch you play, you try getting some extra manpower or load a save without viewers noticing :P

If PDX gives me a possibility to support Ironman, I'll happily include it. 

## Setting up

First up, edit the config.json file with the necessary informations: 
* oauth='oauth:yourOauthToken (from the Bot)' get your oauth token here: https://twitchapps.com/tmi/
* bot='Username of the bot' This needs to be a valid Twitch account you can get the oauth token for
* channel='Channel you want to use it in'
* path='Path to the EU4 Documents path, the one with settings.txt in it, either with \\ or /'
* game='Path to the EU4 Game, containing eu4.exe, either with \\ or /'
* language='english or german'

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
```


## Usage

Simply run 'python app.py' in a terminal and let it run. Currently it supports four commands:

* !ideen (!ideas if language is english)-> gives out the ideas from the player from latest save
* !mods -> gives out the mods from settings.txt with pretty names
* !ae -> gives out the AE (over 10) against the player (takes a few secs) 
* !waffenstillstand (!truces if language is english) -> shows current Truces

If you have questions, please ask.   
If you have suggestions for better performance, more beautiful code ..., please tell me. 

Have fun! 

## Future plans

* Maybe rewrite AE/truces getting method without generator
* I'd wish to read out Ironman files, but not sure how
* maybe add ability to read compressed not-Ironman files