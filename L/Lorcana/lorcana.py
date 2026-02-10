#!/usr/bin/python3

"""
Collection manager/purchase suggester for Lorcana
"""

import os
import re

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Lorcana"

valid_types = ['Character', 'Action', 'Item', 'Location', ]
valid_colors = ['Emerald', 'Ruby', 'Sapphire', 'Steel', 'Amber', 'Amethyst', ]
card_sets = ["The First Chapter", "Rise of the Floodborn", "Into the Inklands", "Ursula's Return",
    "Shimmering Skies", "Azurite Sea", "Archazia's Island", "Reign of Jafar", 'Fabled',
    'Whispers in the Well', 'Winterspell']
valid_rarities = ['Common', 'Uncommon', 'Rare', 'Super Rare', 'Legendary']

def parse_sets(this_card_name, card_set_string):
    """
    The heavy lifting function of this module, where I go through and figure out rarites, sets,
    formats, and anything else
    """
    ret_sets = []
    ret_rarities = set()
    for card_set in card_set_string.split('/'):
        match_obj = re.search(r"(.*) \((.*)\)", card_set)
        if match_obj:
            this_set, this_set_rarity = match_obj.groups()
            if this_set not in card_sets:
                print(f"Invalid card set {this_set} for {this_card_name}")
                continue
            if this_set_rarity not in valid_rarities:
                print(f"Invalid rarity {this_set_rarity} for {this_card_name}")
                continue
            ret_sets.append(this_set)
            ret_rarities.add(this_set_rarity)
    return (ret_sets, list(ret_rarities))

FILE_PREFIX = "card_games/L/Lorcana"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "L/Lorcana"

file_h = open(FILE_PREFIX + '/Data/LorcanaData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
card_names = set()
item_list = []
for line in lines:
    line = line.split('#')[0].strip()
    if line == '':
        continue
    try:
        card_name, card_type, card_color, card_traits, card_set_info, card_own = line.split(';')
    except ValueError:
        print("Issue with line:")
        print(line)
        continue
    if card_name in card_names:
        print("Duplicate card name: " + card_name)
    card_names.add(card_name)
    if card_type not in valid_types:
        print("Invalid card type: " + card_type)
    card_colors = card_color.split('/')
    for card_color in card_colors:
        if card_color not in valid_colors:
            print("Invalid card color: " + card_color)
    card_traits = card_traits.split('/')

    card_own = int(card_own)

    this_card_sets, this_card_rarities = parse_sets(card_name, card_set_info) # pylint: disable=unbalanced-tuple-unpacking

    CARD_MAX = 4
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_type, card_colors, this_card_sets, this_card_rarities, \
        card_own, CARD_MAX))

# Filter by card_set
chosen_set, filtered_list = sort_and_filter(item_list, 3)

#Filter by color
chosen_color, filtered_list = sort_and_filter(filtered_list, 2)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 1)

# Filter by rarity
chosen_rarity, filtered_list = sort_and_filter(filtered_list, 4)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/LorcanaOut.txt", 'w', encoding="UTF-8")

    double_print("Lorcana TCG Inventory Tracker\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)
    SUB_STRING = ' '.join([chosen_rarity, chosen_color, chosen_type])
    CHOICE_STRING = f"Buy {picked_item[0]} ({SUB_STRING}) from {picked_item[3]} (have " + \
        f"{picked_item[5]} out of {picked_item[6]})"
    double_print(CHOICE_STRING, out_file_h)

    out_file_h.close()
