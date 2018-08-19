"""Saving settings"""

import json

SETTINGS = {"Windows": "paperman-win.exe", "Darwin": "paperman-macos", "Linux": "paperman-linux"}

def load_config():
    """
    Load config.json
    :return: Dict
    """
    with open('config.json') as config:
        return json.load(config)


def config_get(item):
    """
    Get information from config.json
    :param item: Json Key
    :return: String
    """
    with open('config.json') as config:
        return json.load(config)[item]
