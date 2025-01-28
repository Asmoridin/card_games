#!/usr/bin/python3

"""
Collection tracker/manager for the Wyvern card game
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "Wyvern"

def get_sets(in_sets):
    """
    Break my set string into a list of sets, and validate them.
    """
    ret_sets = []
    in_sets = in_sets.split('/')
    for in_set in in_sets:
        if in_set in ['Limited', 'Kingdom', 'Premiere Limited', 'Phoenix', 'Chameleon', ]:
            ret_sets.append(in_set)
        else:
            print(in_set)
    return ret_sets

if os.getcwd().endswith('card_games'):
    file_h = open('DB/WyvernData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('card_games/DB/WyvernData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
for line in lines:
    card_name, card_type, card_sets, card_own = line.split(';')
    card_own = int(card_own)
    card_sets = get_sets(card_sets)
    CARD_MAX = 4
    if card_type == 'Dragon':
        CARD_MAX = 2
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_type, card_sets, card_own, CARD_MAX))

# Filter by set
chosen_set, filtered_list = sort_and_filter(item_list, 2)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 1)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

if __name__ == "__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("output/WyvernOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/output/WyvernOut.txt", 'w', encoding="UTF-8")

    double_print("Wyvern CCG Inventory Tracker\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)
    choice_string = f"Buy {picked_item[0]} ({chosen_type}) from {'/'.join(picked_item[2])} " + \
        f"(have {picked_item[3]} out of {picked_item[4]})"
    double_print(choice_string, out_file_h)

    out_file_h.close()
