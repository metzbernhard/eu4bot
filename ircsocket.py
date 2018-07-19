"""opens irc socket and provides send methods"""

import socket
import os
import sys
import logging

import helpers

class IrcSocket:
    """
    Holds connection for IRC and provides IRC methods
    """

    def __init__(self, args):

        self.logger = logging.getLogger(__name__)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Server (not sure why it'd change)
        self.server = 'irc.chat.twitch.tv'

        try:
            print(os.getcwd())
            with open('env.env', 'r') as env:
                text = env.readlines()

            if args.bot:
                self.bot = args.bot
            else:
                self.bot = text[1].strip()[5:-1]

            if args.auth:
                self.auth = args.auth
            else:
                self.auth = text[0].strip()[7:-1]

            if args.channel:
                self.channel = args.channel
            else:
                self.channel = text[2].strip()[9:-1]

            if args.path:
                os.chdir(args.path)
            else:
                os.chdir(text[3].strip()[6:-1])

        except KeyError:
            sys.exit()
        # except:
        #     print("Something is wrong with the provided parameters")
        #     sys.exit()

        # let's connect
        self.logger.info(f"Opening Connection to {self.channel} on Twitch IRC as {self.bot}")
        self.sock.connect((self.server, 6667))

        # now we login and send a test message
        self.sock.send(str.encode('PASS ' + self.auth + '\r\n'))
        self.sock.send(str.encode('NICK ' + self.bot + '\r\n'))
        self.sock.send(str.encode('USER ' + self.bot + '\r\n'))
        self.sock.send(str.encode('JOIN #' + self.channel + '\r\n'))
        # self.sock.send(str.encode('PRIVMSG #' + channel + ' : TEST\r\n'))


    def send_ping(self, send_string):
        """
        Answers PING messages with PONG to keep connection open
        :param send_string:
        """
        self.sock.send(str.encode(send_string))


    def send_msg(self, send_string):
        """
        sends given message to IRC channel
        :param send_string:
        """
        begin = 'PRIVMSG #' + self.channel + ' : '
        end = '\r\n'
        self.logger.info(f"Sending {send_string} to {self.channel} on Twitch IRC as {self.bot}")

        send = begin + send_string + end

        #chopping up  strings too long for single Twitch Messages
        if len(send) < 450:

            self.sock.send(str.encode(send))

        else:

            for line in helpers.chopping(send_string):

                self.sock.send(str.encode(begin + line + end, encoding='UTF-8'))
