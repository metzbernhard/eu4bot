"""Methods to retreive information from save or settings.txt"""

import re
import os
import logging

import helpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ideas():
    """
    Retrieve ideas from savegame
    :return: String
    """
    os.chdir('save games')

    # open latest file
    text = helpers.open_save()

    # get the player's tag
    nation = text[3][8:-2]
    date = text[1]
    logger.info(f"Getting ideas for {nation}")

    #get the line where nation's idea start
    indexes = [i for i in range(len(text)) if nation + '_ideas' in text[i]]
    index = indexes[0]

    temp = []
    line = text[index].strip().replace(nation, 'National')
    temp.append(line)

    #get the rest of the ideas
    while True:
        index = index + 1
        if '}' not in text[index]:
            temp.append(text[index].strip())
        else:
            break

    result = []

    for idea in temp:
        result.append(idea.replace('_', ' ').replace('7', 'Finished').title())
    result.append(date)

    result = ', '.join(result)
    comeon = result + date

    os.chdir('..')

    return comeon


def get_mods():
    """
    Retrieve Mods
    :return: String
    """
    logger.info('getting mods')

    with open('settings.txt', 'r') as f:
        text = f.readlines()
    text = [line.strip()[5:-1] for line in text if 'mod/' in line]
    os.chdir('mod')

    mods = []

    for line in text:
        with open(line, 'r') as mod:
            text = mod.readlines()
        mod = text[0][6:-2]
        if mod.endswith(' [module]'):
            mod = mod[:-9]
        elif mod.endswith(' [Event Window]'):
            mod = mod[:-15]
        mods.append(mod)

    mods = ', '.join(mods)
    mods = mods.replace(' [module]', '')

    os.chdir('..')
    return mods


def get_ae():
    """
    Retrieves AE from Save
    :return: String
    """
    logger.info('Getting Aggressive Expansion')

    # open latest file
    os.chdir('save games')
    text = helpers.open_save()

    ae = {}
    nation, relations, player_relation, our_ae, got_player = False, False, False, False, True
    date = text[1]

    for line in text:

        if got_player and 'player' in line:
            player = line[8:-2]
            got_player = False

        # we start the section for a single nation -> nation = True
        m = re.search('(^[ \t])([A-Z]{3})(={)', line)
        if m:
            tag = m.group(2)
            nation = True
        elif not m and not nation:
            continue

        # we enter the active_relations path for a ntion
        if nation and 'active_relations' in line:
            relations = True

        # in active_relations we look for the player
        elif relations and player in line:
            player_relation = True

        # if we entered the player nation and another tag comes before 'aggressive_expansion'
        # that nation does not have AE and we look for the next
        elif player_relation and re.match('([ \t]*)([A-Z]{3})(={)', line):
            player_relation, nation, relations = False, False, False

        # we are in our relation-section and find aggressive -> look for teh value
        elif player_relation and 'aggressive' in line:
            our_ae = True

        # we found the value!
        elif our_ae and 'current_opinion' in line:
            ae[tag] = line[line.index('=') + 1:].strip()
            nation, relations, player_relation, our_ae = False, False, False, False


    ae_dict = {k: float(v) for k, v in ae.items()}
    ae_name = {helpers.lookup(key):value for (key, value) in ae_dict.items()}

    sorted_ae = sorted(ae_name.items(), key=lambda kv: kv[1])

    ae_string = ""
    for value in sorted_ae:
        if value[1] < -25.0:
            ae_string += (value[0] + ': ' + str(value[1]) + ', ')
    ae_string += (", " + date)

    os.chdir('..')
    return ae_string


def get_truces():
    """
    Retries Truces
    :return: String
    """
    logging.info('Getting Truces')

    # open latest file
    os.chdir('save games')
    text = helpers.open_save()

    tags = []
    date = text[1]
    player, got_tag, active, playersection, got_player = False, False, False, False, False

    for line in text:

        if not got_player and 'player' in line:
            player = line[8:-2]
            got_player = True

        if not player:
            continue

        # looking for the players section
        m = re.search('(^[ \t])(' + player + ')(={)', line)
        if m:
            playersection = True
            continue

        if not playersection:
            continue

        if 'active_relations' in line:
            active = True

        if active:
            m = re.search('([ \t]*)([A-Z]{3})(={)', line)
            if m:
                tag = m.group(2)
                got_tag = True

        if got_tag and 'truce' in line:

            tags.append(tag)

        elif got_tag and re.match('([ \t]*)([A-Z]{3})(={)', line):

            m = re.search('([ \t]*)([A-Z]{3})(={)', line)
            if m:
                tag = m.group(2)
                got_tag = True

        if playersection and 'decision_seed' in line:
            break


    truces = [helpers.lookup(tag) for tag in tags]
    truces.append(date)
    truces = ', '.join(truces)

    os.chdir('..')
    return truces


if __name__ == '__main__':
    pass
