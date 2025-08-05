#!/usr/bin/python3

"""
Collection tracker and purchase suggestion tool for the Anachronism card game
"""

import os

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Anachronism"

valid_nations = ['Mongol', 'Carthaginian', 'Greek', 'Roman', 'Tribes of Israel', 'Korean',
    'Chinese', 'Japanese', 'Romanian', 'Persian', 'Trojan', 'Germanic', 'Native American',
    'Aztec', 'Egyptian', 'American Frontiersmen', 'Pirate', 'Scottish', 'Briton', 'Maori',
    'Turkish', 'Irish', 'Norse', 'Russian', 'Spanish', 'East Indian', 'Byzantine', 'French',
    'Welsh', 'Italian', 'African Kingdoms', 'Saracen', 'German', 'Holy Roman', 
]
valid_types = ['Armor', 'Weapon', 'Warrior', 'Inspiration', 'Special']

FILE_PREFIX = "card_games/A/Anachronism"

if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "A/Anachronism"

OUT_FILE_NAME = FILE_PREFIX + "/AnachronismOut.txt"

with open(FILE_PREFIX + '/Data/AnachronismData.txt', 'r', encoding="UTF-8") as file_h:
    lines = file_h.readlines()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
warriors_own = [0, 0]
for line in lines:
    line = line.split('//')[0]
    try:
        card_name, in_nation, card_type, card_set, card_max, card_own = line.split(';')
    except ValueError:
        print("Problem with line")
        print(line)
        continue
    card_own = int(card_own)
    card_max = int(card_max)
    card_nation = []
    for nation in in_nation.split('/'):
        if nation not in valid_nations:
            print("Invalid Nation: " + nation)
        card_nation.append(nation)
    if card_type not in valid_types and card_type != '':
        print(f"Invalid card type: {card_type}")
    if card_type == 'Warrior':
        warriors_own[1] += card_max
        warriors_own[0] += card_own
    TOTAL_MAX += card_max
    TOTAL_OWN += card_own
    item_list.append((card_name, card_nation, card_type, card_set, card_own, card_max))

chosen_nation, filtered_list = sort_and_filter(item_list, 1)
chosen_set, filtered_list = sort_and_filter(filtered_list, 3)
_, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

if __name__=="__main__":
    with open(OUT_FILE_NAME, 'w', encoding="UTF-8") as out_file_h:
        double_print("Anachronism card game Inventory Tracker Tool\n", out_file_h)

        total_string = f"Have {TOTAL_OWN} of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
        double_print(total_string, out_file_h)
        CHOICE_STRING = f"Buy {picked_item[0]} ({'/'.join(picked_item[1])}) from " + \
            f"{picked_item[3]} (have {picked_item[4]} out of {picked_item[5]})"
        double_print(CHOICE_STRING, out_file_h)

        double_print(f"\nOwn {warriors_own[0]} out of {warriors_own[1]} warrior cards.",out_file_h)
