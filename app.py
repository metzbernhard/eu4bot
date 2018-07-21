"""This module starts a forever running Python bot for EU4"""

import logging
import argparse

import getinfo
import helpers
from ircsocket import IrcSocket

def main():
    """
    Main method to get started
    opens connection and starts endless while loop for polling IRC Channel
    """

    args = parse()

    game = args.game if args.game else helpers.config_get("game")
    language = args.language if args.language else helpers.config_get("language")

    commands = {'truces': '!truces', 'ideas': '!ideas', 'ae': '!ae', 'mods': '!mods'}
    if language == 'german':
        commands['truces'] = '!waffenstillstand'
        commands['ideas'] = '!ideen'

    # do some logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logging.info(commands)

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

        # ignore messages that aren't commands
        # only catches commmands if at the beginning of the message
        elif ':!' not in text:
            pass

        else:
            try:
                user = text[text.index('!') + 1:text.index('@')]
            except ValueError:
                continue
                #some default twitch messages don't fit the bill, but don't give us a user anyway

            text = text[text.rfind(':') + 1:].strip()

            # get ideas
            if text.startswith(commands.get('ideas')):

                connection.send_msg(user.title() + ': ' + getinfo.get_ideas())

            #get mods from settings
            elif text.startswith(commands.get('mods')):

                connection.send_msg(user.title() + ': ' + getinfo.get_mods())

            #get ae
            elif text.startswith(commands.get('ae')):

                connection.send_msg(user.title() + ': ' + getinfo.get_ae(game, language))

            #get truces
            elif text.startswith(commands.get('truces')):

                connection.send_msg(user.title() + ': ' + getinfo.get_truces(game, language))


def parse():
    """
    Recovers arguments from the commandline
    :return:
    """
    parser = argparse.ArgumentParser(description='EU4 IRC Bot')

    parser.add_argument('-b', dest='bot', action='store', help='Twitch Account used as bot')
    parser.add_argument('-c', dest='channel', action='store', help='Channel you want to use')
    parser.add_argument('-o', dest='auth', action='store', help='oauth "oauth:oauth_token"')
    parser.add_argument('-p', dest='path', action='store', help='Path to the settings.txt')
    parser.add_argument('-g', dest='game', action='store', help='Path to the EU4 Game-Directory')
    parser.add_argument('-l', dest='language', action='store', help='english or german')

    return parser.parse_args()


if __name__ == '__main__':
    main()
