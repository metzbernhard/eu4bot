"""Helper functions"""
import os

def lookup(game, tag):
    """
    Looks up nation names for tags
    :param game:
    :param tag:
    :return:
    """

    temp = os.getcwd()
    os.chdir(os.path.join(game, 'localisation'))

    with open('countries_l_german.yml', 'r', encoding='UTF-8') as f:
        text = f.readlines()

    nation = ""

    for line in text:
        if tag in line:
            nation = line.strip()[7:-1]
            break

    if nation == '':
        with open('text_l_german.yml', 'r', encoding='UTF-8') as f:
            text = f.readlines()
        for line in text:
            if '\n ' + tag in line:
                nation = line.strip()[7:-1]
                break

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
