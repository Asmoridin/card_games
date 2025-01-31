#!/usr/bin/python3

"""
Tracker and army suggestion tool for games of Dragon Dice
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index
from card_games.list_scripts import dragon_dice

if os.getcwd().endswith('card_games'):
    out_file_h = open("wl_output/DragonDiceWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/DragonDiceResults.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("card_games/wl_output/DragonDiceWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('card_games/wl_data/DragonDiceResults.txt', 'r', encoding="UTF-8")

double_print("Dragon Dice Win-Loss Tracker and army selector\n", out_file_h)
all_armies = dragon_dice.army_factions
my_armies = dragon_dice.my_current_factions

data_lines = in_file.readlines()
in_file.close()
data_lines = [line.strip() for line in data_lines]

army_games_map = {} # Total number of games I've seen the army
for army in all_armies:
    army_games_map[army] = 0

my_army_wl = {}
my_opp_wl = {}
my_opp_army_wl = {}
total_wl = [0, 0]

for line in data_lines:
    if line == "":
        continue
    if line.startswith('#'):
        continue
    my_army, opp_army, opponent, w_l = line.split(';')

    if my_army not in all_armies:
        double_print(f"Invalid army: {my_army}", out_file_h)
    if opp_army not in all_armies:
        double_print(f"Invalid army: {opp_army}", out_file_h)

    army_games_map[my_army] += 1
    army_games_map[opp_army] += 1

    if w_l not in ['W', 'L']:
        double_print(f"Invalid W/L: {w_l}", out_file_h)

    if my_army not in my_army_wl:
        my_army_wl[my_army] = [0, 0]
    if opponent not in my_opp_wl:
        my_opp_wl[opponent] = [0, 0]
    if opp_army not in my_opp_army_wl:
        my_opp_army_wl[opp_army] = [0, 0]

    if w_l == 'W':
        my_army_wl[my_army][0] += 1
        my_opp_wl[opponent][0] += 1
        total_wl[0] += 1
        my_opp_army_wl[opp_army][0] += 1
    if w_l == 'L':
        my_army_wl[my_army][1] += 1
        my_opp_wl[opponent][1] += 1
        total_wl[1] += 1
        my_opp_army_wl[opp_army][1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
double_print("My record by army:", out_file_h)
for army in sorted(my_army_wl):
    double_print(f"{army}: {my_army_wl[army][0]}-{my_army_wl[army][1]}", out_file_h)

army_h_index = []
for army, l_w_l in my_army_wl.items():
    army_h_index.append((army, sum(l_w_l)))
army_h_index = sorted(army_h_index, key=lambda x:x[1], reverse=True)

double_print(f"\nMy H-Index is {get_h_index(army_h_index)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent in sorted(my_opp_wl):
    double_print(f"{opponent}: {my_opp_wl[opponent][0]}-{my_opp_wl[opponent][1]}", out_file_h)

double_print("\nMy record against opposing armies:", out_file_h)
for opp_army in sorted(my_opp_army_wl):
    ldr_str = f"{opp_army}: {my_opp_army_wl[opp_army][0]}-{my_opp_army_wl[opp_army][1]}"
    double_print(ldr_str, out_file_h)

MIN_SEEN = 1000000
min_seen_armies = []
for army, army_games in army_games_map.items():
    if army_games < MIN_SEEN:
        MIN_SEEN = army_games
        min_seen_armies = [army]
    elif army_games == MIN_SEEN:
        min_seen_armies.append(army)
double_print(f"\nI've seen these armies on the table the least ({MIN_SEEN} times): " + \
    f"{'; '.join(sorted(min_seen_armies))}", out_file_h)

playable_army_list = []
for army in my_armies:
    if army not in my_army_wl:
        playable_army_list.append((army, 0))
    else:
        playable_army_list.append((army, sum(my_army_wl[army])))
playable_army_list = sorted(playable_army_list, key=lambda x:(x[1], x[0]))
least_army = playable_army_list[0][0]
least_army_games = playable_army_list[0][1]

sugg_string = f"\nI should play more games with {least_army}, as I only have " + \
    f"{least_army_games} game{('', 's')[least_army_games != 1]}"
double_print(sugg_string, out_file_h)
