#!/usr/bin/python3

"""
Collection manager/purchase suggester for the Gundam GCG
"""

import os

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Gundam Card Game"

valid_types = ['Unit', 'Command', 'Base', 'Pilot', ]
valid_colors = ['Red', 'Blue', 'Green', 'White', 'Purple']

FILE_PREFIX = "card_games/G/Gundam_Card_Game"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "G/Gundam_Card_Game"

file_h = open(FILE_PREFIX + '/Data/Gundam GCG Card Data.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
champions = set()
for line in lines:
    line = line.split('#')[0].strip()
    try:
        card_name, card_number, card_rarity, card_block, card_lvl, card_cost, card_color, \
            card_type, card_traits, card_sets, card_own = line.split(';')
    except ValueError:
        print("Invalid line:")
        print(line)
        continue

    if card_type not in valid_types:
        print(f"Invalid card type {card_type} for {card_name}")
    if card_color not in valid_colors:
        print(f"Invalid card color {card_color} for {card_name}")
    card_own = int(card_own)
    CARD_MAX = 4
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_number, card_rarity, card_block, card_lvl, card_cost, \
        card_color, card_type, card_traits, card_sets, card_own, CARD_MAX))

#Filter by set
chosen_set, filtered_list = sort_and_filter(item_list, 9)

# Filter by card_color
chosen_color, filtered_list = sort_and_filter(filtered_list, 6)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 7)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/Gundam GCG Out.txt", 'w', encoding="UTF-8")

    double_print("Gundam Card Game Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    SUGG_STRING = f"Buy {picked_item[0]} ({chosen_color + ' ' + chosen_type}) from " + \
        f"{picked_item[1]} (have {picked_item[10]} out of {picked_item[11]})"
    double_print(SUGG_STRING, out_file_h)

    out_file_h.close()
