#!/usr/bin/python3

"""
Collection manager/tracker for the Tribbles card game
"""

import os
from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Tribbles"

FILE_PREFIX = "card_games/T/Tribbles"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "T/Tribbles"
file_h = open(FILE_PREFIX + '/Data/TribblesData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
card_names = set()
card_lines = []
filter_lines = []

for line in lines:
    line = line.split('//')[0].strip()
    card_name, card_type, card_sets, max_item, own_item = line.split(';')
    if card_name in card_names:
        print("Duplicate: " + card_name)
    card_names.add(card_name)
    max_item = int(max_item)
    own_item = int(own_item)
    if card_type == 'Tribble':
        card_count, card_power = card_name.split('-')
        card_count = card_count.strip()
        card_power = card_power.strip()
        card_lines.append((card_count, card_power, own_item, max_item))
    elif card_type == 'Trouble':
        pass
    TOTAL_MAX += max_item
    TOTAL_OWN += own_item

# Figure out appropriate Tribble power
chosen_power, filtered_list = sort_and_filter(card_lines, 1)

# Filter and sort by quantity
chosen_qty, filtered_list = sort_and_filter(filtered_list, 0)

if __name__ == "__main__":
    OUT_FILENAME = FILE_PREFIX + "/TribblesOut.txt"
    out_file_h = open(OUT_FILENAME, 'w', encoding="UTF-8")

    double_print("Tribbles Inventory Tracker\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)
    card_pct = (filtered_list[0][2]/filtered_list[0][3]) * 100
    purch_str = f"Next purchase sould be {chosen_qty} - {chosen_power}, where I have " + \
        f"{card_pct:.2f} percent"
    double_print(purch_str, out_file_h)
