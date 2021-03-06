"""Helper functions"""
import os
import json
import logging
from subprocess import call

from settings import SETTINGS as settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def lookup(tag):
    """
    Looks up nation names for tags
    :param game:
    :param tag:
    :return:
    """

    temp = os.getcwd()
    os.chdir(os.path.join(settings["game"], 'localisation'))

    with open(f'countries_l_{settings["language"]}.yml', 'r', encoding='UTF-8') as f:
        text = f.readlines()

    nation = ''

    for line in text:
        if tag in line:
            nation = line.strip()[7:-1]
            break

    # for some reason 55 of the over 600 tags are in text_l_ ...
    if nation == '':
        with open(f'text_l_{settings["language"]}.yml', 'r', encoding='UTF-8') as f:
            text = f.readlines()
        for line in text:
            if '\n ' + tag in line:
                nation = line.strip()[7:-1]
                break

    # still not found? no idea
    if nation == '':
        nation = tag

    os.chdir(temp)
    return nation


def chopping(long_string):
    """
    Twitch won't let you send messages > 500
    :param long_string:
    :return:
    """
    texts = []
    start, index = 0, 0
    while index >= 0:
        index = long_string.find(',', start + 450)
        if index > 0:
            texts.append(long_string[start:index])
        else:
            texts.append(long_string[start:])
            break
        start = index

    return texts


def config_get(item):
    """
    Get information from config.json
    :param item: Json Key
    :return: String
    """
    with open('config.json') as config:
        return json.load(config)[item]


def load_config():
    """
    Load config.json
    :return: Dict
    """
    with open('config.json') as config:
        return json.load(config)


def open_save():
    """
    Open Save, either ironman or not
    :return: text
    """
    save = max(os.listdir(), key=os.path.getctime)
    logger.info("Opening " + save)
    logger.info(settings["ironman"])
    if settings["ironman"]=='True' and not 'paperman' in save:
        try:
            call([os.path.join(settings["app_dir"], settings["paperman"]), save])
            save = max(os.listdir(), key=os.path.getctime)
        except FileNotFoundError:
            logger.error("It seems you did not provide paperman for removing Ironman. "
                         "Please download it at https://gitgud.io/nixx/paperman"
                         " and put it into the directory with app.py")

    with open(save, 'r') as f:
        text = f.readlines()

    return text
