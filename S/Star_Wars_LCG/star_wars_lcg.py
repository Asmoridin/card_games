#!/usr/bin/python3

"""
Different than my usual system- my plan here is actually to just look through and validate decks
by different eras, mention sets/cards I don't see used, and things like that.  Not likely part
of the larger CCG system.
"""

import os
from itertools import combinations
from card_games.General.Libraries.output_utils import double_print

GAME_NAME = "Star Wars LCG"

FILE_PREFIX = "card_games/S/Star_Wars_LCG"

if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "S/Star_Wars_LCG"

DECK_DIR = FILE_PREFIX + "/Decks"
OUT_FILE_NAME = FILE_PREFIX + "/Star Wars LCG.txt"
CARDS_FILENAME = FILE_PREFIX + '/Data/Star Wars LCG Cards.txt'
USED_TRAIT_FILENAME = FILE_PREFIX + '/Data/Star Wars LCG Used Traits.txt'
SET_INDICES_FILENAME = FILE_PREFIX + '/Data/Set Indices.txt'

CYCLES = ['01 - Core Set', '02 - Hoth Cycle', '03 - Echoes of the Force Cycle',
    '04 - Rogue Squadron Cycle', '05 - Endor Cycle', '06 - Opposition Cycle',
    '07 - Alliances Cycle']

DS_AFFILS = ['Imperial Navy', 'Sith', 'Dark Neutral', 'Scum and Villainy']
LS_AFFILS = ['Rebel Alliance', 'Jedi', 'Smugglers and Spies', 'Light Neutral']
VALID_AFFILIATIONS = DS_AFFILS + LS_AFFILS
SIDE_MAPPING = {}
for push_affil in VALID_AFFILIATIONS:
    if push_affil in DS_AFFILS:
        SIDE_MAPPING[push_affil] = "DS"
    else:
        SIDE_MAPPING[push_affil] = "LS"

CARD_TYPES = ['Unit', 'Objective', 'Event', 'Enhancement', 'Fate', 'Mission']

# Read in objective data
with open(FILE_PREFIX + '/Data/Star Wars LCG Objectives.txt', 'r', encoding="UTF-8") as obj_file:
    obj_lines = obj_file.readlines()
obj_lines = [line.strip() for line in obj_lines]
objectives = {}
obj_count = {}
obj_side = {}
for obj_line in obj_lines:
    AFF_ONLY = "No"
    if obj_line.count(';') == 3:
        obj_name, obj_affil, obj_set, obj_max = obj_line.split(';')
    else:
        obj_name, obj_affil, obj_set, obj_max, AFF_ONLY = obj_line.split(';')
    if obj_affil not in VALID_AFFILIATIONS:
        print(f"{obj_name} has an invalid affiliation of {obj_affil}")
    obj_max = int(obj_max)
    objectives[obj_name] = (obj_affil, obj_set, obj_max)
    obj_count[obj_name] = 0
    if obj_affil in ['Imperial Navy', 'Sith', 'Dark Neutral', 'Scum and Villainy']:
        obj_side[obj_name] = 'DS'
    else:
        obj_side[obj_name] = 'LS'

# Read in the cards
objective_num_to_name = {}
card_lines = []
cards_with_trait = {"DS":{}, "LS":{}}
with open(CARDS_FILENAME, 'r', encoding="UTF-8") as card_fh:
    for card_line in card_fh:
        if card_line.startswith('#'):
            continue
        card_line = card_line.strip()
        try:
            card_name, card_affil, card_type, card_traits, card_cost, force_icons, \
                obj_sets = card_line.split(';')
        except ValueError:
            print(f"Issue with line {card_line}")
            continue
        if card_affil not in VALID_AFFILIATIONS:
            print(f"{card_name} seems to have an invalid affiliation of {card_affil}")
            continue
        if card_type not in CARD_TYPES:
            print(f"{card_name} seems to have an invalid type of {card_type}")
            continue
        if card_traits != '':
            for trait in card_traits.split('/'):
                if trait not in cards_with_trait[SIDE_MAPPING[card_affil]]:
                    cards_with_trait[SIDE_MAPPING[card_affil]][trait] = 0
                cards_with_trait[SIDE_MAPPING[card_affil]][trait] += 1
        if card_type == 'Objective':
            this_obj_set = obj_sets.split('-')[0]
            objective_num_to_name[this_obj_set] = card_name
        card_lines.append(card_line)

TOTAL_OWN = 0
for card_item in card_lines:
    obj_sets = card_item.split(';')[-1]
    for this_obj_set in obj_sets.split('/'):
        obj_num, obj_quant = this_obj_set.split('-')
        obj_quant = int(obj_quant)
        max_obj = objectives[objective_num_to_name[obj_num]][2]
        TOTAL_OWN += (max_obj * obj_quant)
TOTAL_MAX = TOTAL_OWN

with open(USED_TRAIT_FILENAME, 'r', encoding="UTF-8") as used_traits:
    trait_lines = used_traits.readlines()
    for trait_line in trait_lines:
        if trait_line.startswith('#'):
            continue
        trait_name, trait_side = trait_line.strip().split(';')
        if trait_side not in ['DS', 'LS', 'Both']:
            print(f"Invalid Used Trait side of {trait_side}")
        if trait_side in ['DS', 'Both']:
            if trait_name not in cards_with_trait['DS']:
                print(f"Trait {trait_name} doesn't seem to be a valid DS trait")
            else:
                del cards_with_trait['DS'][trait_name]
        if trait_side in ['LS', 'Both']:
            if trait_name not in cards_with_trait['LS']:
                print(f"Trait {trait_name} doesn't seem to be a valid LS trait")
            else:
                del cards_with_trait['LS'][trait_name]

set_index_lines = []
with open(SET_INDICES_FILENAME, 'r', encoding="UTF-8") as set_fh:
    set_index_lines = set_fh.readlines()
print(set_index_lines)

def get_index(in_deck):
    """
    Determine a set's index, and allow me some validation ability
    """
    ret_index = 0
    if in_deck['Affiliation'] != "" and in_deck['Affiliation'] not in VALID_AFFILIATIONS:
        if in_deck['Affiliation'] in ['Mercenary Contacts']:
            return 6
        print(f"Need to handle index for affilation {in_deck['Affiliation']}")
    for objective_set_name, obj_set_qty in in_deck['Objectives'].items():
        if objective_set_name not in objectives:
            print(f"Need data on {objective_set_name}")
            continue
        obj_count[objective_set_name] += 1
        if obj_set_qty > objectives[objective_set_name][2]:
            print(f"{in_deck['Deck Name']} has a likely illegal amount of objective " + \
                f"set {objective_set_name}")
        this_card_set = objectives[objective_set_name][1]
        if this_card_set == 'Core Set':
            pass
        elif this_card_set in ['The Desolation of Hoth', 'The Search For Skywalker',
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
        if this_deck_line == "Affiliation: Rebel Alliance":
            ret_deck['Affiliation'] = "Rebel Alliance"
            continue
        if this_deck_line == "Affiliation: Scum and Villainy":
            ret_deck['Affiliation'] = "Scum and Villainy"
            continue
        if this_deck_line == "Affiliation: Sith":
            ret_deck['Affiliation'] = "Sith"
            continue
        if this_deck_line == "Affiliation: Mercenary Contacts":
            ret_deck['Affiliation'] = "Mercenary Contacts"
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
        no_affil_str = f"List {side + '/' + deck_era + '/' + deck_filename} has no Affiliation"
        print(no_affil_str)
    return ret_deck

def compare_decks(list_of_decks):
    """
    Do an analysis of each deck to determine if any decks are the same
    """
    check_combos = list(combinations(list_of_decks, 2))
    for combo in check_combos:
        if combo[0]['Objectives'] == combo[1]['Objectives']:
            print("Duplicate?:")
            print(combo[0]['Deck Name'])
            print(combo[1]['Deck Name'])

for side in os.listdir(DECK_DIR):
    DECK_ERA_CHECK = -1
    side_decks = []
    for deck_era in os.listdir(DECK_DIR + "/" + side):
        DECK_ERA_CHECK += 1
        era_dir = DECK_DIR + "/" + side + "/" + deck_era
        for deck_filename in os.listdir(era_dir):
            MAX_INDEX = 0
            with open(era_dir + "/" + deck_filename, 'r', encoding="UTF-8") as deck_fh:
                deck_lines = deck_fh.readlines()
            deck_lines = [line.strip() for line in deck_lines]
            this_deck = read_deck(deck_lines, side + "/" + deck_era + "/" + deck_filename)
            side_decks.append(this_deck)
            MAX_INDEX = get_index(this_deck)
            if MAX_INDEX > DECK_ERA_CHECK:
                full_deck_name = side + "/" + deck_era + "/" + deck_filename
                print(f"Deck {full_deck_name} needs to move to a higher category - in " + \
                    f"{CYCLES[DECK_ERA_CHECK]}, should be {CYCLES[MAX_INDEX]}")
    compare_decks(side_decks)

if __name__ == "__main__":
    out_fh = open(OUT_FILE_NAME, 'w', encoding="UTF-8")
    double_print(f"The Star Wars LCG has {len(card_lines)} distinct cards", out_fh)
    double_print(f"A full collection has {TOTAL_OWN} cards.\n", out_fh)

    double_print("Top 10 unused traits by side:", out_fh)
    double_print("Dark Side:", out_fh)
    unused_traits = cards_with_trait['DS'].items()
    unused_traits = sorted(unused_traits, reverse = True, key=lambda x:(x[1], x[0]))
    for unused_trait in unused_traits[:10]:
        double_print(f" - {unused_trait[0]}: {unused_trait[1]}", out_fh)

    double_print("Light Side:", out_fh)
    unused_traits = cards_with_trait['LS'].items()
    unused_traits = sorted(unused_traits, reverse = True, key=lambda x:(x[1], x[0]))
    for unused_trait in unused_traits[:10]:
        double_print(f" - {unused_trait[0]}: {unused_trait[1]}", out_fh)

    PRINTED_HEADER = False
    for obj_set_name, obj_set_amount in sorted(obj_count.items()):
        if obj_set_amount == 0:
            if not PRINTED_HEADER:
                double_print("\nUnused objective sets:", out_fh)
                PRINTED_HEADER = True
            double_print(f" - {obj_set_name} ({obj_side[obj_set_name]})", out_fh)
