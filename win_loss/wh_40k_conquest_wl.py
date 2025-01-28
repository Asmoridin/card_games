#!/usr/bin/python3

"""
Win-Loss tracker and Warlord suggestion tool for Warhammer 40K: Conquest
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index

if os.getcwd().endswith('card_games'):
    out_file_h = open("wl_output/WH40KConquestOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/WH40KConquestWL.txt', 'r', encoding="UTF-8")
    warlord_data_file = open('wl_data/WH40KConquestWarlords.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("card_games/wl_output/WH40KConquestOut.txt", 'w', encoding="UTF-8")
    in_file = open('card_games/wl_data/WH40KConquestWL.txt', 'r', encoding="UTF-8")
    warlord_data_file = open('card_games/wl_data/WH40KConquestWarlords.txt', 'r', encoding="UTF-8")

double_print("Warhammer 40K: Conquest Win-Loss Tracker and warlord selector", out_file_h)

# Let's read the warlords, and parse the warlord data
warlords_by_faction = {}
warlord_to_faction = {}
warlord_total_plays = {}
seen_total = {}
warlord_lines = warlord_data_file.readlines()
warlord_data_file.close()
warlord_lines = [line.strip() for line in warlord_lines]
for warlord_line in warlord_lines:
    if warlord_line == '':
        continue
    try:
        warlord_name, faction = warlord_line.split(';')
    except ValueError:
        print("Issue with warlord line:")
        print(warlord_line)
        continue
    if faction not in warlords_by_faction:
        warlords_by_faction[faction] = []
    warlord_to_faction[warlord_name] = faction
    warlords_by_faction[faction].append(warlord_name)
    warlord_total_plays[warlord_name] = 0
    seen_total[warlord_name] = 0

# Let's start parsing the W-L data
warlord_wl = {} # For each warlord, the total win-loss
faction_wl = {} # For each faction, its win-loss
opp_wl = {} # Win-Loss-Tie by opponent
opp_faction_wl = {} # W-L for each faction
total_wl = [0, 0]
in_lines = in_file.readlines()
in_file.close()
in_lines = [line.strip() for line in in_lines]
for line in in_lines:
    if line == '':
        continue
    try:
        my_warlord, opp_warlord, opp_name, result = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if my_warlord not in seen_total:
        print(f"My warlord not recognized: {my_warlord}")
        continue
    if opp_warlord not in seen_total:
        print(f"Opponent's warlord not recognized: {opp_warlord}")
        continue
    if result not in ['W', 'L']:
        print("Invalid response in line:")
        print(line)
        continue
    if my_warlord not in warlord_wl:
        warlord_wl[my_warlord] = [0, 0]
    seen_total[my_warlord] += 1
    warlord_total_plays[my_warlord] += 1

    seen_total[opp_warlord] += 1
    my_faction = warlord_to_faction[my_warlord]
    opp_faction = warlord_to_faction[opp_warlord]

    if my_faction not in faction_wl:
        faction_wl[my_faction] = [0, 0]
    if opp_name not in opp_wl:
        opp_wl[opp_name] = [0, 0]
    if opp_faction not in opp_faction_wl:
        opp_faction_wl[opp_faction] = [0, 0]
    if result == 'W':
        total_wl[0] += 1
        warlord_wl[my_warlord][0] += 1
        faction_wl[my_faction][0] += 1
        opp_wl[opp_name][0] += 1
        opp_faction_wl[opp_faction][0] += 1
    elif result == 'L':
        total_wl[1] += 1
        warlord_wl[my_warlord][1] += 1
        faction_wl[my_faction][1] += 1
        opp_wl[opp_name][1] += 1
        opp_faction_wl[opp_faction][1] += 1

double_print(f"My current record (W-L) is {total_wl[0]}-{total_wl[1]}", out_file_h)

double_print(f"\nMy record by warlord: ({len(seen_total)} total warlords in game)", out_file_h)
warlord_play_tuples = []
for faction, faction_ids in sorted(warlords_by_faction.items()):
    faction_wl_str = f"{faction}:"
    if faction in faction_wl:
        faction_wl_str = f"{faction}: {faction_wl[faction][0]}-{faction_wl[faction][1]}"
    double_print(faction_wl_str, out_file_h)
    for w_name in faction_ids:
        if w_name in warlord_wl:
            warlord_play_tuples.append((w_name, sum(warlord_wl[w_name])))
            out_str = f" - {w_name}: {warlord_wl[w_name][0]}-{warlord_wl[w_name][1]}"
            double_print(out_str, out_file_h)

warlord_play_tuples = sorted(warlord_play_tuples, key=lambda x: (-1 * x[1], x[0]))
double_print(f"\nMy H-Index is {get_h_index(warlord_play_tuples)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent, this_opp_wl in sorted(opp_wl.items()):
    opp_wl_str = f"- {opponent}: {this_opp_wl[0]}-{this_opp_wl[1]}"
    double_print(opp_wl_str, out_file_h)

double_print("\nMy record against opposing factions:", out_file_h)
for opp_faction, faction_wl in sorted(opp_faction_wl.items()):
    faction_wl_str = f"- {opp_faction}: {faction_wl[0]}-{faction_wl[1]}"
    double_print(faction_wl_str, out_file_h)

# Least seen Warlord
LEAST_PLAYED_QTY = 100
least_played_ids = []
for warlord_name, id_played in seen_total.items():
    if id_played < LEAST_PLAYED_QTY:
        LEAST_PLAYED_QTY = id_played
        least_played_ids = [warlord_name]
    elif id_played == LEAST_PLAYED_QTY:
        least_played_ids.append(warlord_name)

double_print("\nI've seen the following warlords on the table the least " + \
        f"({LEAST_PLAYED_QTY} times)", out_file_h)
double_print(", ".join(least_played_ids), out_file_h)

# Figure out least played relevant warlord
faction_plays = {}
filtered_warlord_plays = []
for check_id, warlord_plays in warlord_total_plays.items():
    this_faction = warlord_to_faction[check_id]
    filtered_warlord_plays.append((check_id, warlord_plays))
    if this_faction not in faction_plays:
        faction_plays[this_faction] = 0
    faction_plays[this_faction] += warlord_plays
faction_play_sorter = []
for this_faction, faction_plays in faction_plays.items():
    faction_play_sorter.append((this_faction, faction_plays))
faction_play_sorter = sorted(faction_play_sorter, key=lambda x:(x[1], x[0]))

LOWEST_faction = faction_play_sorter[0]
relevant_warlord_plays = []

for warlord_name, warlord_plays in filtered_warlord_plays:
    if warlord_to_faction[warlord_name] == LOWEST_faction[0]:
        relevant_warlord_plays.append((warlord_name, warlord_plays))
relevant_warlord_plays = sorted(relevant_warlord_plays, key=lambda x:(x[1], x[0]))

low_warlord = relevant_warlord_plays[0]
LOW_O_STR = f"\nI should play more games with {LOWEST_faction[0]}, where I only have " + \
    f"{int(LOWEST_faction[1])} games. Suggested warlord - {low_warlord[0]} ({low_warlord[1]} " + \
    "total plays)"
double_print(LOW_O_STR, out_file_h)
