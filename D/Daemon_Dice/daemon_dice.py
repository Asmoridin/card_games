#!/usr/bin/python3

"""
Collection tracker/purchase suggestions for Daemon Dice
"""

import os

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Daemon Dice"

if os.getcwd().endswith('card_games'):
    file_h = open('DaemonDiceData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('card_games/D/Daemon_Dice/Data/DaemonDiceData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
for line in lines:
    dice_demon, dice_part, own = line.split(';')
    own = int(own)
    dice_max = max(own, 5)
    TOTAL_MAX += dice_max
    TOTAL_OWN += own
    item_list.append((dice_demon, dice_part, own, dice_max))

# Filter by faction
chosen_faction, filtered_list = sort_and_filter(item_list, 0)

# Filter by body part
chosen_part, filtered_list = sort_and_filter(filtered_list, 1)

pick_list = []
for item in filtered_list:
    if item[1] == chosen_part:
        pick_list.append(item)
pick_list = sorted(pick_list, key=lambda x:(x[2]/x[3], -1*(x[2]-x[2]), x[0] + ' ' + x[1]))
picked_item = pick_list[0]
#print(picked_item)

if __name__=="__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("Daemon_Dice/DaemonDiceOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/D/Daemon_Dice/DaemonDiceOut.txt", 'w', encoding="UTF-8")

    double_print("Daemon Dice Inventory Tracker Tool\n", out_file_h)

    inv_str = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100*TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(inv_str, out_file_h)
    buy_str = f"Buy a {picked_item[0] + ' ' + picked_item[1]} (have {picked_item[2]} " + \
        f"out of {picked_item[3]})"
    double_print(buy_str, out_file_h)

    out_file_h.close()
