import re
import os

def get_ideas():

    os.chdir('save games')

    save = max(os.listdir(), key=os.path.getctime)
    with open (save, 'r') as f:
        text = f.readlines()

    nation = text[3][8:-2]
    indexes = [i for i in range(len(text)) if nation + '_ideas' in text[i]]
    index = indexes[0]

    temp = []
    line = text[index].strip()
    temp.append(line)

    while True:
        index = index + 1
        if '}' not in text[index]:
            temp.append(text[index].strip())
        else:
            break

    result = []

    for idea in temp:
        result.append(idea.replace('_', ' ').replace('7', 'Finished').title())

    result = ', '.join(result)

    os.chdir('..')
    return result


def get_mods():

    with open ('settings.txt', 'r') as f:
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

    # for chopping the message if too long
    # texts = []
    # start, index = 0, 0
    # while index >= 0:
    #     index = mods.find(',', start + 500)
    #     if index > 0:
    #         texts.append(mods[start:index])
    #     else:
    #         texts.append(mods[start:])
    #         break
    #     start = index

    os.chdir('..')
    return mods


def get_ae():

    os.chdir('save games')
    save = max(os.listdir(), key=os.path.getctime)

    nations = []
    ae = {}
    nation, relations, ath_relation, our_ae, got_player = False, False, False, False, True

    with open(save, 'r') as f:

        for line in f:

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
                ath_relation = True

            # if we entered the player nation and another tag comes before 'aggressive_expansion' that nation does not have AE and we look for the next
            elif ath_relation and re.match('([ \t]*)([A-Z]{3})(={)', line):
                ath_relation, nation, relations = False, False, False


            # we are in our relation-section and find aggressive -> look for teh value
            elif ath_relation and 'aggressive' in line:
                our_ae = True


            # we found the value!
            elif our_ae and 'current_opinion' in line:
                # print(tag)
                # print(line[line.index('=')+1:].strip())
                # print('~~~~~~~~~~~~~~~')
                ae[tag] = line[line.index('=') + 1:].strip()

                nation, relations, ath_relation, our_ae = False, False, False, False

    ae = {k: float(v) for k, v in ae.items()}
    sorted_ae = sorted(ae.items(), key=lambda kv: kv[1])

    ae = ""
    for value in sorted_ae:
        if value[1] < -10.0:
            ae += (value[0] + ': ' + str(value[1]) + ', ')

    os.chdir('..')
    return (ae)


def get_truces():

    os.chdir('save games')
    save = max(os.listdir(), key=os.path.getctime)

    tags = []

    player, got_tag, active, playersection, got_player = False, False, False, False, False

    with open(save, 'r') as f:

        for line in f:

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

            # m = re.search('(^[ \t])([A-Z]{3})(={)', line)

            if playersection and 'decision_seed' in line:
                break

    truces = ', '.join(tags)

    os.chdir('..')
    return(truces)