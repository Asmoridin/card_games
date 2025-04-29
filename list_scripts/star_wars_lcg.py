#!/usr/bin/python3

"""
Different than my usual system- my plan here is actually to just look through and validate decks
by different eras, mention sets/cards I don't see used, and things like that.  Not likely part
of the larger CCG system.
"""

import os

from steve_utils.output_utils import double_print

GAME_NAME = "Star Wars LCG"

if os.getcwd().endswith('card_games'):
    file_h = open('DB/Star Wars LCG Data.txt', 'r', encoding="UTF-8")
    DECK_DIR = "Decks/Star Wars LCG"
    OUT_FILE_NAME = "output/Star Wars LCG.txt"
else:
    file_h = open('card_games/DB/Star Wars LCG Data.txt', 'r', encoding="UTF-8")
    DECK_DIR = "card_games/Decks/Star Wars LCG"
    OUT_FILE_NAME = "card_games/output/Star Wars LCG.txt"

CYCLES = ['01 - Core Set', '02 - Hoth Cycle', '03 - Echoes of the Force Cycle',
    '04 - Rogue Squadron Cycle', '05 - Endor Cycle', '06 - Opposition Cycle',
    '07 - Alliances Cycle']

VALID_AFFILIATIONS = ['Imperial Navy', 'Sith', 'Rebel Alliance', 'Jedi', 'Dark Neutral',
    'Smugglers and Spies', 'Light Neutral', 'Scum and Villainy', ]

out_fh = open(OUT_FILE_NAME, 'w', encoding="UTF-8")

# Read in objective data
obj_lines = file_h.readlines()
file_h.close()
obj_lines = [line.strip() for line in obj_lines]
objectives = {}
for obj_line in obj_lines:
    obj_name, obj_affil, obj_set, obj_max = obj_line.split(';')
    if obj_affil not in VALID_AFFILIATIONS:
        print(f"{obj_name} has an invalid affiliation of {obj_affil}")
    obj_max = int(obj_max)
    objectives[obj_name] = (obj_affil, obj_set, obj_max)

def get_index(in_deck):
    """
    Determine a set's index, and allow me some validation ability
    """
    ret_index = 0
    if in_deck['Affiliation'] != "":
        if in_deck['Affiliation'] not in VALID_AFFILIATIONS:
            print(f"Need to handle index for affilation {in_deck['Affiliation']}")
    for objective_set_name, obj_set_qty in in_deck['Objectives'].items():
        if objective_set_name not in objectives:
            print(f"Need data on {objective_set_name}")
        else:
            if obj_set_qty > objectives[objective_set_name][2]:
                print(f"{in_deck['Deck Name']} has a likely illegal amount of objective " + \
                    f"set {objective_set_name}")
            this_card_set = objectives[objective_set_name][1]
            if this_card_set == 'Core Set':
                pass
            elif this_card_set in ['The Desolation of Hoth', 'The Search for Skywalker',
                    'A Dark Time', 'Assault on Echo Base', 'The Battle of Hoth',
                    'Escape from Hoth', 'Edge of Darkness']:
                ret_index = max(ret_index, 1)
            elif this_card_set in ['Balance of the Force', 'Heroes and Legends',
                    'Lure of the Dark Side', 'Knowledge and Defense', 'Join Us or Die',
                    'It Binds All Things', 'Darkness and Light']:
                ret_index = max(ret_index, 2)
            elif this_card_set in ['Between the Shadows', 'Ready for Takeoff',
                    'Draw Their Fire', 'Evasive Maneuvers', 'Attack Run',
                    'Chain of Command', 'Jump to Lightspeed']:
                ret_index = max(ret_index, 3)
            elif this_card_set in ['Imperial Entanglements', "Solo's Command",
                    'New Alliances', 'The Forest Moon', 'So Be It',
                    'Press the Attack', 'Redemption and Return']:
                ret_index = max(ret_index, 4)
            elif this_card_set in ['Galactic Ambitions', "Ancient Rivals",
                    'A Wretched Hive', 'Meditation and Mastery', 'Scrap Metal',
                    'Power of the Force', 'Technological Terror']:
                ret_index = max(ret_index, 5)
            elif this_card_set in ['Allies of Necessity', "Aggressive Negotiations",
                    'Desperate Circumstances', 'Swayed by the Dark Side',
                    'Trust in the Force', 'Promise of Power']:
                ret_index = max(ret_index, 5)
            else:
                print(f"Need to figure out location of {this_card_set}")
    return ret_index

def read_deck(in_deck_lines, deck_name):
    """
    Read in a deck, do some validation
    """
    ret_deck = {}
    ret_deck['Affiliation'] = ""
    ret_deck['Objectives'] = {}
    ret_deck['Deck Name'] = deck_name
    for this_deck_line in in_deck_lines:
        if this_deck_line.startswith('//') or this_deck_line == "":
            continue
        if this_deck_line == "Affiliation: Imperial Navy":
            ret_deck['Affiliation'] = "Imperial Navy"
            continue
        if this_deck_line == "Affiliation: Smugglers and Spies":
            ret_deck['Affiliation'] = "Smugglers and Spies"
            continue
        if this_deck_line == "Affiliation: Jedi":
            ret_deck['Affiliation'] = "Jedi"
            continue
        try:
            deck_obj_qty = int(this_deck_line.split(' ')[0])
            deck_obj = ' '.join(this_deck_line.split(' ')[1:])
            if deck_obj == "":
                print(f"Unhandled line in deck {deck_name}:")
                print(this_deck_line)
            ret_deck['Objectives'][deck_obj] = deck_obj_qty
        except ValueError:
            print(f"Unhandled line in deck {deck_name}:")
            print(this_deck_line)
    if ret_deck['Affiliation'] == "":
        no_affil_str = f"List {side + "/" + deck_era + "/" + deck_filename} has no Affiliation"
        double_print(no_affil_str, out_fh)
    return ret_deck

for side in os.listdir(DECK_DIR):
    DECK_ERA_CHECK = -1
    for deck_era in os.listdir(DECK_DIR + "/" + side):
        DECK_ERA_CHECK += 1
        era_dir = DECK_DIR + "/" + side + "/" + deck_era
        for deck_filename in os.listdir(era_dir):
            MAX_INDEX = 0
            deck_fh = open(era_dir + "/" + deck_filename, 'r', encoding="UTF-8")
            deck_lines = deck_fh.readlines()
            deck_fh.close()
            deck_lines = [line.strip() for line in deck_lines]
            this_deck = read_deck(deck_lines, side + "/" + deck_era + "/" + deck_filename)
            MAX_INDEX = get_index(this_deck)
            if MAX_INDEX > DECK_ERA_CHECK:
                full_deck_name = side + "/" + deck_era + "/" + deck_filename
                print(f"Deck {full_deck_name} needs to move to a higher category - in " + \
                    f"{CYCLES[DECK_ERA_CHECK]}, should be {CYCLES[MAX_INDEX]}")
