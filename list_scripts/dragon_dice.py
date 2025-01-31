#!/usr/bin/python3

"""
Collection tracker/purchase suggester for Dragon Dice
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "Dragon Dice"

army_factions = ['Dwarves', 'Coral Elves', 'Goblins', 'Lava Elves', 'Amazons', 'Fire Walkers',
    'Undead', 'Feral', 'Swamp Stalkers', 'Frostwings', 'Scalders', 'Treefolk', 'Eldarim',
    'Dracolem']
valid_factions = army_factions + ['Medallion', 'Items', 'Dragons', 'Dragonkin', 'Relics',
    'Major Terrain', 'Minor Terrain', 'Special Terrain']

my_current_factions = ['Frostwings', 'Fire Walkers', 'Treefolk', ]
my_future_factions = ['Swamp Stalkers', 'Undead', 'Scalders', 'Goblins', 'Feral',
    'Dwarves', 'Coral Elves', 'Lava Elves', 'Amazons', 'Eldarim', 'Dracolem']

def get_meta_type(in_type):
    """
    Take in a type of dice, and then return a more general dice group
    """
    if in_type in army_factions:
        return 'Unit'
    if in_type in ['Special Terrain', 'Major Terrain', 'Minor Terrain']:
        return 'Terrain'
    if in_type in ['Items', 'Medallion', 'Relics']:
        return 'Item'
    if in_type in ['Dragons', 'Dragonkin']:
        return 'Dragon'
    print("Unhandled meta type: " + in_type)
    return 'Unhandled'

if os.getcwd().endswith('card_games'):
    file_h = open('DB/DragonDiceCollection.txt', 'r', encoding="UTF-8")
else:
    file_h = open('card_games/DB/DragonDiceCollection.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
faction_total = {}
for line in lines:
    dice_name, dice_faction, dice_size, own = line.split(';')
    if dice_faction not in valid_factions:
        print("Invalid faction: " + dice_faction)
    own = int(own)
    DICE_MAX = 1
    if dice_faction not in faction_total:
        faction_total[dice_faction] = 0
    if dice_size == "Rare":
        if dice_faction in ['Items', 'Dragonkin']:
            DICE_MAX = max(own, 1)
        else:
            DICE_MAX = max(own, 2)
        faction_total[dice_faction] += (own * 3)
    elif dice_size == "Uncommon":
        if dice_faction in ['Items', 'Dragonkin']:
            DICE_MAX = max(own, 2)
        else:
            DICE_MAX = max(own, 4)
        faction_total[dice_faction] += (own * 2)
    elif dice_size == "Common":
        if dice_faction in ['Items', 'Dragonkin']:
            DICE_MAX = max(own, 4)
        else:
            DICE_MAX = max(own, 8)
        faction_total[dice_faction] += (own)
    elif dice_size in ["Monster", "Champion", "Artifact", "Dragon"]:
        DICE_MAX = max(own, 1)
        faction_total[dice_faction] += (own * 4)
    elif dice_faction == "Major Terrain":
        DICE_MAX = max(own, 2)
    elif dice_faction in ['Minor Terrain', 'Special Terrain']:
        DICE_MAX = max(own, 1)
    else:
        print("Unhandled dice size: " + dice_size)
    META_TYPE = get_meta_type(dice_faction)
    TOTAL_MAX += DICE_MAX
    TOTAL_OWN += own
    item_list.append((dice_name, dice_faction, META_TYPE, dice_size, own, DICE_MAX))

chosen_meta, filtered_list = sort_and_filter(item_list, 2)

# If we are going to choose units, I want to ensure I'm choosing the right faction
faction_map = {}
if chosen_meta == 'Unit':
    for die_tuple in filtered_list:
        if die_tuple[1] not in my_current_factions:
            continue
        if die_tuple[1] not in faction_map:
            faction_map[die_tuple[1]] = [0, 0]
        faction_map[die_tuple[1]][0] += die_tuple[4]
        faction_map[die_tuple[1]][1] += die_tuple[5]
    fac_list = []
    for map_fac, map_inv in faction_map.items():
        fac_list.append((map_fac, map_inv[0], map_inv[1]))
    fac_list = sorted(fac_list, key=lambda x:(x[1]/x[2], x[0]))
    FILTERED_FACTION = fac_list[0][0]
    if (len(my_current_factions) / len(army_factions)) < (fac_list[0][1] / fac_list[0][2]):
        FILTERED_FACTION = my_future_factions[0]
    new_list = []
    for check_line in filtered_list:
        if check_line[1] == FILTERED_FACTION:
            new_list.append(check_line)
    filtered_list = new_list

chosen_faction, filtered_list = sort_and_filter(filtered_list, 1)
chosen_size, filtered_list = sort_and_filter(filtered_list, 3)
_, filtered_list = sort_and_filter(filtered_list, 0)

picked_item = filtered_list[0]

if __name__=="__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("output/DragonDiceOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/output/DragonDiceOut.txt", 'w', encoding="UTF-8")

    double_print("Dragon Dice Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    next_buy_string = f"Buy a {picked_item[2]} from {picked_item[1]} - perhaps a {picked_item[0]}"
    double_print(next_buy_string, out_file_h)

    double_print("\nPoints for each army:", out_file_h)
    for faction in sorted(army_factions):
        if faction_total[faction] > 0:
            double_print(f"- {faction}: {faction_total[faction]}", out_file_h)

    out_file_h.close()
