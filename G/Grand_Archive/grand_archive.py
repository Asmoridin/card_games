#!/usr/bin/python3

"""
Collection manager/purchase suggester for the Grand Archive TCG
"""

import os

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Grand Archive TCG"

valid_subtypes = ['Ally', 'Action', 'Champion', 'Regalia Weapon', 'Regalia Item', 'Attack',
    'Domain', 'Item', 'Regalia Ally', 'Phantasia', 'Weapon', 'Mastery']
valid_classes = ['Cleric', 'Warrior', 'Ranger', 'Mage', 'Assassin', 'Guardian', 'Tamer',
    'Warrior', 'Spirit', ]
valid_elements = ['Norm', 'Fire', 'Water', 'Wind', 'Luxem', 'Arcane', 'Tera', 'Umbra',
    'Neos', 'Astra', 'Crux', 'Exia',]

FILE_PREFIX = "card_games/G/Grand_Archive"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "G/Grand_Archive"

file_h = open(FILE_PREFIX + '/Data/GrandArchiveData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
card_names = set()
item_list = []
champions = set()
for line in lines:
    line = line.split('#')[0].strip()
    TEMP_MAX = 0
    if line.count(';') == 5:
        card_name, card_sets, card_subtype, card_class, card_element, card_own = line.split(';')
    elif line.count(';') == 6:
        card_name, card_sets, card_subtype, card_class, card_element, \
            card_own, TEMP_MAX = line.split(';')
        TEMP_MAX = int(TEMP_MAX)
    else:
        print("Invalid line:")
        print(line)
        continue
    if card_name in card_names:
        print("Duplicate card name: " + card_name)
    card_names.add(card_name)
    if card_subtype not in valid_subtypes:
        print("Invalid card subtype: " + card_subtype)
    card_class = card_class.split('/')
    for in_class in card_class:
        if in_class not in valid_classes:
            print("Invalid card class: " + in_class)
    if card_element not in valid_elements:
        print("Invalid card element: " + card_element)
    card_own = int(card_own)

    CARD_MAX = 4
    if card_subtype in ['Champion', 'Regalia Weapon', 'Regalia Item', 'Regalia Ally']:
        CARD_MAX = 1
    if 'Champion' in card_subtype and not card_name.startswith('Spirit of') and not \
        card_name.startswith('Fragmented Spirit of') and card_name != "Prismatic Spirit":
        champions.add(card_name.split(',')[0])
    if TEMP_MAX != 0:
        CARD_MAX = TEMP_MAX
    if card_own > CARD_MAX:
        CARD_MAX = card_own
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_sets, card_subtype, card_class, card_element, \
        card_own, CARD_MAX))

# Filter by card_class
chosen_class, filtered_list = sort_and_filter(item_list, 3)

#Filter by subtype
chosen_subtype, filtered_list = sort_and_filter(filtered_list, 2)

#Filter by element
chosen_element, filtered_list = sort_and_filter(filtered_list, 4)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/GrandArchiveOut.txt", 'w', encoding="UTF-8")

    double_print("Grand Archive TCG Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    double_print(f"{len(champions)} different champions in the game\n", out_file_h)

    sugg_string = f"Buy {picked_item[0]} ({chosen_class + ' ' + chosen_subtype}) from " + \
        f"{picked_item[1]} (have {picked_item[5]} out of {picked_item[6]})"
    double_print(sugg_string, out_file_h)

    out_file_h.close()
