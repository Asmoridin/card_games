#!/usr/bin/python3

"""
Collection manager/purchase suggester for Riftbound
"""

import os

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Riftbound"

valid_types = ['Unit', 'Spell', 'Battlefield', 'Legend', 'Champion Unit', 'Gear', 'Rune',
    'Signature Spell', 'Signature Unit',]
valid_colors = ['Chaos', 'Body', 'Mind', 'Order', 'Fury', 'Colorless', 'Calm']

FILE_PREFIX = "card_games/R/Riftbound"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "R/Riftbound"

file_h = open(FILE_PREFIX + '/Data/Riftbound Data.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
legends = set()
for line in lines:
    line = line.split('#')[0].strip()
    try:
        card_name, card_type, card_color, card_traits, card_cost, card_power, card_might, \
            card_sets, card_own = line.split(';')

    except ValueError:
        print("Invalid line:")
        print(line)
        continue

    if card_type not in valid_types:
        print(f"Invalid card type {card_type} for {card_name}")
    if card_type == 'Legend':
        legends.add(card_name)
    card_colors = card_color.split('/')
    for card_color in card_colors:
        if card_color not in valid_colors:
            print(f"Invalid card color {card_color} for {card_name}")
    card_traits = card_traits.split('/')
    card_own = int(card_own)
    CARD_MAX = 3
    if card_type == 'Legend':
        CARD_MAX = 1
    elif card_type == 'Battlefield':
        CARD_MAX = 2
    elif card_type == 'Relic':
        CARD_MAX = 12
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_type, card_colors, card_traits, card_cost, card_power, \
            card_might, card_sets, card_own, CARD_MAX))

#Filter by set
chosen_set, filtered_list = sort_and_filter(item_list, 7)

# Filter by card_color
chosen_color, filtered_list = sort_and_filter(filtered_list, 2)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 1)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/Riftbound Out.txt", 'w', encoding="UTF-8")

    double_print("Riftbound Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    double_print(f"{len(legends)} different legends in the game\n", out_file_h)

    SUGG_STRING = f"Buy {picked_item[0]} ({chosen_color + ' ' + chosen_type}) from " + \
        f"{picked_item[7]} (have {picked_item[8]} out of {picked_item[9]})"
    double_print(SUGG_STRING, out_file_h)

    out_file_h.close()
