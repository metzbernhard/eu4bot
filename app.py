import time
import getinfo
import logging
from irc_socket import irc_socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# we connect to irc using environment values
connection = irc_socket()

# this'll run as long as you don't kill it
while 1:
    text = connection.sock.recv(2040).decode()

    logger.info(text)

    # answer pings to stay connected
    if 'PING' in text:
        logger.info('Answer ping')
        connection.sendping('PONG :tmi.twitch.tv\r\n')

    # ignore messages that aren' commands, [30: because irc comands have a ! too
    elif '!' not in text[30:]:
        pass

    else:
        try:
            user = text[text.index('!') + 1:text.index('@')]
            # fails for some default messages, that don't matter
        except:
            user = ""

        text = text[text.rfind(':') + 1:].strip()

        # get ideas
        if text.startswith('!ideen'):

            connection.send_msg(user.title() + ': ' + getinfo.get_ideas())

        #get mods from settings
        elif text.startswith('!mods'):

            connection.send_msg(user.title() + ': ' + getinfo.get_mods())

        #get ae
        elif text.startswith('!ae'):

            connection.send_msg(user.title() + ': ' + getinfo.get_ae())

        #get truces
        elif text.startswith('!waffenstillstand'):

            connection.send_msg(user.title() + ': ' + getinfo.get_truces())