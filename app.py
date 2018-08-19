"""This module starts a forever running Python bot for JakeChat on IRC"""

import logging
import argparse
import os
import platform

import getinfo
import helpers
from settings import SETTINGS as settings
from ircsocket import IrcSocket

def main():
    """
    Main method to get started
    opens connection and starts endless while loop for polling IRC Channel
    """

    # get arguments from command line
    args = parse()

    # set our settings for this run
    settings["app_dir"] = os.getcwd()
    settings["paperman"] = settings[platform.system()]
    settings["channel"] = args.game if args.game else helpers.config_get("channel")
    settings["game"] = args.game if args.game else helpers.config_get("game")
    settings["ironman"] = args.ironman if args.ironman else helpers.config_get("ironman")
    settings["language"] = args.language if args.language else helpers.config_get("language")

    # do some logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # open connection
    connection = IrcSocket(args)

    # this'll run as long as you don't kill it
    while 1:
        text = connection.sock.recv(2040).decode()
        logger.info(text)

        # answer pings to stay connected
        if 'PING' in text:
            logger.info('Answer ping')
            connection.send_ping('PONG :tmi.twitch.tv\r\n')

        # don't you dare try using commands
        elif ' :!' in text:
            try:
                user = text[text.index('!') + 1:text.index('@')]
                logger.info(user)
            except ValueError:
                continue
                #some default twitch messages don't fit the bill, but don't give us a user anyway

            connection.timeout(user, 10)
            connection.send_whisper("No public bot commands here, whisper me 'commands'.", user)


        # one public info command
        # elif 'WHISPER' not in text:
        #     if ':!ryukyubot' in text:
        #         connection.send_msg("Whisper 'commands' to ryukyubot for more information")
        #         continue

        elif 'WHISPER' in text:
            try:
                user = text[text.index('!') + 1:text.index('@')]
            except ValueError:
                continue
                #some default twitch messages don't fit the bill, but don't give us a user anyway

            text = text[text.rfind(':') + 1:].strip()

            # commands
            if text.startswith('commands'):

                connection.send_whisper("Whisper me 'ideas', 'ae', 'truces', 'mods' or 'uptime'", user)

            # get ideas
            elif text.startswith('ideas'):

                connection.send_whisper(getinfo.get_ideas(), user)

            #get mods from settings
            elif text.startswith('mods'):

                connection.send_whisper(getinfo.get_mods(), user)

            #get ae
            elif text.startswith('ae'):

                connection.send_whisper(getinfo.get_ae(), user)

            #get truces
            elif text.startswith('truces'):

                connection.send_whisper(getinfo.get_truces(), user)

            #questions?
            elif text.startswith('uptime'):

                connection.send_whisper(getinfo.uptime(), user)

        else:
            continue



def parse():
    """
    Get arguments from the commandline
    :return: args
    """
    parser = argparse.ArgumentParser(description='IRC Quote Bot')

    parser.add_argument('-b', dest='bot', action='store', help='Twitch Account used as bot')
    parser.add_argument('-c', dest='channel', action='store', help='Channel you want to use')
    parser.add_argument('-o', dest='auth', action='store', help='oauth "oauth:oauth_token"')
    parser.add_argument('-p', dest='path', action='store', help='Path to the settings.txt')
    parser.add_argument('-g', dest='game', action='store', help='Path to the EU4 Game-Directory')
    parser.add_argument('-l', dest='language', action='store', help='english or german')
    parser.add_argument('-i', dest='ironman', action='store_true', help='ironman-flag')

    return parser.parse_args()


if __name__ == '__main__':
    main()
