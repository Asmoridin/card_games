#!/usr/bin/python3

"""
Win-Loss tracker and OUTFIT suggestion tool for Doomtown: Reloaded
"""

import os

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.get_h_index import get_h_index

FILE_PREFIX = "card_games/D/Doomtown_Reloaded"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "D/Doomtown_Reloaded"

out_file_h = open(FILE_PREFIX + "/DoomtownOut.txt", 'w', encoding="UTF-8")
in_file = open(FILE_PREFIX + '/Data/DoomtownData.txt', 'r', encoding="UTF-8")
outfit_data_file = open(FILE_PREFIX + '/Data/DoomtownOutfits.txt', 'r', encoding="UTF-8")

CURRENT_FORMAT = "Weird West Edition"
VALID_GANGS = ['Anarchists','Law Dogs','Entrepreneurs','Fearmongers','First Peoples','Outlaws']

double_print("Doomtown: Reloaded Win-Loss Tracker and deck selector", out_file_h)

# Let's read the OUTFITs, and parse the OUTFIT data
outfits = {'Weird West Edition':{}, 'Old Timer':{}}
outfits_by_gang = {}
outfit_to_gang = {}
outfit_total_plays = {}
seen_total = {}
outfit_lines = outfit_data_file.readlines()
outfit_data_file.close()
outfit_lines = [line.strip() for line in outfit_lines]
for outfit_line in outfit_lines:
    if outfit_line == '':
        continue
    try:
        outfit_name, OUTFIT_GANG, outfit_format = outfit_line.split(';')
    except ValueError:
        print("Issue with outfit line:")
        print(outfit_line)
        continue
    if OUTFIT_GANG not in VALID_GANGS:
        print(f"Unknown gang {OUTFIT_GANG} for outfit {outfit_name}")
        continue
    if outfit_format not in ['Weird West Edition', 'Old Timer']:
        print(f"Unknown format {outfit_format} for outfit {outfit_name}")
        continue
    if OUTFIT_GANG not in outfits_by_gang:
        outfits_by_gang[OUTFIT_GANG] = []
    outfits_by_gang[OUTFIT_GANG].append(outfit_name)
    outfit_to_gang[outfit_name] = OUTFIT_GANG
    outfit_total_plays[outfit_name] = 0
    seen_total[outfit_name] = 0
    do_formats = ['Old Timer']
    if outfit_format == 'Weird West Edition':
        do_formats.append('Weird West Edition')
    for do_format in do_formats:
        if OUTFIT_GANG not in outfits[do_format]:
            outfits[do_format][OUTFIT_GANG] = []
        outfits[do_format][OUTFIT_GANG].append(outfit_name)

# Let's start parsing the W-L data
outfit_wl = {} # For each OUTFIT, the total win loss
gang_wl = {} # For each gang, it's win-loss
opp_wl = {} # Win-Loss by opponent
opp_gang_wl = {} # W-L against each gang
total_wl = [0, 0]
in_lines = in_file.readlines()
in_file.close()
in_lines = [line.strip() for line in in_lines]
for line in in_lines:
    if line == '':
        continue
    try:
        my_outfit, opp_outfit, opp_name, result = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if my_outfit not in outfit_to_gang:
        print(f"My outfit not recognized: {my_outfit}")
        continue
    if opp_outfit not in outfit_to_gang:
        print(f"Opponent's outfit not recognized: {opp_outfit}")
        continue
    my_gang = outfit_to_gang[my_outfit]
    opp_gang = outfit_to_gang[opp_outfit]
    if result not in ['W', 'L']:
        print("Invalid response in line:")
        print(line)
        continue
    if my_outfit not in outfit_wl:
        outfit_wl[my_outfit] = [0, 0]
    seen_total[my_outfit] += 1
    seen_total[opp_outfit] += 1
    if my_gang not in gang_wl:
        gang_wl[my_gang] = [0, 0]
    if opp_name not in opp_wl:
        opp_wl[opp_name] = [0, 0]
    if opp_gang not in opp_gang_wl:
        opp_gang_wl[opp_gang] = [0, 0]
    if result == 'W':
        total_wl[0] += 1
        outfit_wl[my_outfit][0] += 1
        gang_wl[my_gang][0] += 1
        opp_wl[opp_name][0] += 1
        opp_gang_wl[opp_gang][0] += 1
        outfit_total_plays[my_outfit] += 1
    if result == 'L':
        total_wl[1] += 1
        outfit_wl[my_outfit][1] += 1
        gang_wl[my_gang][1] += 1
        opp_wl[opp_name][1] += 1
        opp_gang_wl[opp_gang][1] += 1
        outfit_total_plays[my_outfit] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}", out_file_h)

double_print(f"\nMy record by outfit: ({len(outfit_to_gang)} total outfits in game)", out_file_h)
outfit_play_tuples = []
for gang, gang_ids in sorted(outfits_by_gang.items()):
    gang_wl_str = f"{gang}:"
    if gang in gang_wl:
        gang_wl_str = f"{gang}: {gang_wl[gang][0]}-{gang_wl[gang][1]}"
    double_print(gang_wl_str, out_file_h)
    for outfit_name in gang_ids:
        if outfit_name in outfit_wl:
            outfit_play_tuples.append((outfit_name, sum(outfit_wl[outfit_name])))
            out_str = f" - {outfit_name}: {outfit_wl[outfit_name][0]}-{outfit_wl[outfit_name][1]}"
            double_print(out_str, out_file_h)

outfit_play_tuples = sorted(outfit_play_tuples, key=lambda x: (-1 * x[1], x[0]))
double_print(f"\nMy H-Index is {get_h_index(outfit_play_tuples)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent, this_opp_wl in sorted(opp_wl.items()):
    opp_wl_str = f"- {opponent}: {this_opp_wl[0]}-{this_opp_wl[1]}"
    double_print(opp_wl_str, out_file_h)

double_print("\nMy record against opposing gangs:", out_file_h)
for opp_gang, gang_wl in sorted(opp_gang_wl.items()):
    gang_wl_str = f"- {opp_gang}: {gang_wl[0]}-{gang_wl[1]}"
    double_print(gang_wl_str, out_file_h)

# Least seen OUTFITs
LEAST_PLAYED_QTY = 100
least_played_ids = []
for outfit_name, id_played in seen_total.items():
    if id_played < LEAST_PLAYED_QTY:
        LEAST_PLAYED_QTY = id_played
        least_played_ids = [outfit_name]
    elif id_played == LEAST_PLAYED_QTY:
        least_played_ids.append(outfit_name)

double_print(f"\nI've seen the following outfits on the table the least ({LEAST_PLAYED_QTY} times)",
    out_file_h)
double_print(", ".join(least_played_ids), out_file_h)

# Figure out least played relevant outfit
gang_plays = {}
filtered_outfit_plays = []
for check_id, outfit_plays in outfit_total_plays.items():
    this_gang = outfit_to_gang[check_id]
    if check_id in outfits[CURRENT_FORMAT][this_gang]:
        filtered_outfit_plays.append((check_id, outfit_plays))
        if this_gang not in gang_plays:
            gang_plays[this_gang] = 0
        gang_plays[this_gang] += outfit_plays
gang_play_sorter = []
for this_gang, gang_plays in gang_plays.items():
    gang_play_sorter.append((this_gang, gang_plays))
gang_play_sorter = sorted(gang_play_sorter, key=lambda x:(x[1], x[0]))

LOWEST_GANG = gang_play_sorter[0]
relevant_outfit_plays = []

for outfit_name, outfit_plays in filtered_outfit_plays:
    if outfit_to_gang[outfit_name] == LOWEST_GANG[0]:
        relevant_outfit_plays.append((outfit_name, outfit_plays))
relevant_outfit_plays = sorted(relevant_outfit_plays, key=lambda x:(x[1], x[0]))

double_print(f"\nFollowing are limited to my current format ({CURRENT_FORMAT})", out_file_h)
low_outfit = relevant_outfit_plays[0]
LOW_O_STR = f"I should play more games with {LOWEST_GANG[0]}, where I only have " + \
    f"{int(LOWEST_GANG[1])} games. Suggested outfit - {low_outfit[0]} ({low_outfit[1]} " + \
    "total plays)"
double_print(LOW_O_STR, out_file_h)
