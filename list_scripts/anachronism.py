#!/usr/bin/python3

"""
Collection tracker and purchase suggestion tool for the Anachronism card game
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "Anachronism"

valid_nations = ['Mongol', 'Carthaginian', 'Greek', 'Roman', 'Tribes of Israel', 'Korean',
    'Chinese', 'Japanese', 'Romanian', 'Persian', 'Trojan', 'Germanic', 'Native American',
    'Aztec', 'Egyptian', 'American Frontiersmen', 'Pirate', 'Scottish', 'Briton', 'Maori',
    'Turkish', 'Irish', 'Norse', 'Russian', 'Spanish', 'East Indian', 'Byzantine', 'French',
    'Welsh', 'Italian', 'African Kingdoms', 'Saracen', 'German', 'Holy Roman', 
]

if os.getcwd().endswith('card_games'):
    file_h = open('DB/AnachronismData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('card_games/DB/AnachronismData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
for line in lines:
    line = line.split('//')[0]
    card_name, in_nation, card_set, card_max, card_own = line.split(';')
    card_own = int(card_own)
    card_max = int(card_max)
    card_nation = []
    for nation in in_nation.split('/'):
        if nation not in valid_nations:
            print("Invalid Nation: " + nation)
        card_nation.append(nation)
    TOTAL_MAX += card_max
    TOTAL_OWN += card_own
    item_list.append((card_name, card_nation, card_set, card_own, card_max))

chosen_nation, filtered_list = sort_and_filter(item_list, 1)

chosen_set, filtered_list = sort_and_filter(filtered_list, 2)

pick_list = []
for item in filtered_list:
    if item[2] == chosen_set:
        pick_list.append(item)
pick_list = sorted(pick_list, key=lambda x:(x[3]/x[4], -1*(x[3]-x[3]), x[0]))
picked_item = pick_list[0]

if __name__=="__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("output/AnachronismOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/output/AnachronismOut.txt", 'w', encoding="UTF-8")

    double_print("Anachronism card game Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)
    choice_string = f"Buy {picked_item[0]} ({'/'.join(picked_item[1])}) from {picked_item[2]} " + \
        f"(have {picked_item[3]} out of {picked_item[4]})"
    double_print(choice_string, out_file_h)

    out_file_h.close()
