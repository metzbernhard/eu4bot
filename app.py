"""This module starts a forever running Python bot for EU4"""

import logging
import argparse

import getinfo
from ircsocket import IrcSocket

def main():
    """
    Main method to get started
    opens connection and starts endless while loop for polling IRC Channel
    """

    args = parse()

    if args.game:
        game = args.game
    else:
        with open('env.env', 'r') as file:
            text = file.readlines()
        game = text[4].strip()[6:-1]

    # do some logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # open connection
    connection = IrcSocket(args)

    # this'll run as long as you don't kill it
    while 1:
        text = connection.sock.recv(2040).decode()
        # logger.info(text)

        # answer pings to stay connected
        if 'PING' in text:
            logger.info('Answer ping')
            connection.send_ping('PONG :tmi.twitch.tv\r\n')

        # ignore messages that aren't commands, [30: because irc commands have a ! too
        elif '!' not in text[30:]:
            pass

        else:
            try:
                user = text[text.index('!') + 1:text.index('@')]
            except ValueError:
                continue
                #some default twitch messages don't fit the bill, but don't give us a user anyway

            text = text[text.rfind(':') + 1:].strip()

            # get ideas
            if text.startswith('!ideen'):

                connection.send_msg(user.title() + ': ' + getinfo.get_ideas())

            #get mods from settings
            elif text.startswith('!mods'):

                connection.send_msg(user.title() + ': ' + getinfo.get_mods())

            #get ae
            elif text.startswith('!ae'):

                connection.send_msg(user.title() + ': ' + getinfo.get_ae(game))

            #get truces
            elif text.startswith('!waffenstillstand'):

                connection.send_msg(user.title() + ': ' + getinfo.get_truces(game))


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

    return parser.parse_args()


if __name__ == '__main__':
    main()
