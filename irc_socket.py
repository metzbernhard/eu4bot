import socket
import os
import sys

class irc_socket:

    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Server (not sure why it'd change)
        self.server = 'irc.chat.twitch.tv'

        try:
            with open('env.env', 'r') as f:
                text = f.readlines()
            self.pw = text[0].strip()[7:-1]
            self.bot = text[1].strip()[5:-1]
            self.channel = text[2].strip()[9:-1]
            os.chdir(text[3].strip()[6:-1])
            print(self.pw, self.bot, self.channel)
        except KeyError:
            sys.exit()

        # let's connect
        self.sock.connect((self.server, 6667))

        # now we login and send a test message
        self.sock.send(str.encode('PASS ' + self.pw + '\r\n'))
        self.sock.send(str.encode('NICK ' + self.bot + '\r\n'))
        self.sock.send(str.encode('USER ' + self.bot + '\r\n'))
        self.sock.send(str.encode('JOIN #' + self.channel + '\r\n'))
        # self.sock.send(str.encode('PRIVMSG #' + channel + ' : TEST\r\n'))


    def send_ping(self, send_string):
        self.sock.send(str.encode(send_string))

    def send_msg(self, send_string):
        start = 'PRIVMSG #' + self.channel + ' : '
        end = '\r\n'
        self.sock.send(str.encode(start + send_string + end))
