#!/usr/bin/python3

"""
Win-Loss tracker and Leader suggestion too for 7th Sea: City of Five Sails
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index

if os.getcwd().endswith('card_games'):
    out_file_h = open("wl_output/7thSeaCo5SOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/7thSeaCo5SWL.txt', 'r', encoding="UTF-8")
    ldr_data_file = open('wl_data/7thSeaCo5SLeaders.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("card_games/wl_output/7thSeaCo5SOut.txt", 'w', encoding="UTF-8")
    in_file = open('card_games/wl_data/7thSeaCo5SWL.txt', 'r', encoding="UTF-8")
    ldr_data_file = open('card_games/wl_data/7thSeaCo5SLeaders.txt', 'r', encoding="UTF-8")

VALID_FACTIONS = ['Castille', 'Eisen', 'Montaigne', 'Ussura', 'Vodacce']

double_print("7th Sea: City of Five Sails Win-Loss Tracker and leader selector", out_file_h)

# Let's read the leaders, and parse the leader data
ldrs_by_faction = {}
ldr_to_faction = {}
ldr_total_plays = {}
seen_total = {}
ldr_lines = ldr_data_file.readlines()
ldr_data_file.close()
ldr_lines = [line.strip() for line in ldr_lines]
for ldr_line in ldr_lines:
    if ldr_line == '':
        continue
    try:
        faction, ldr_name = ldr_line.split(';')
    except ValueError:
        print("Issue with leader line:")
        print(ldr_line)
        continue
    if faction not in VALID_FACTIONS:
        print(f"Unknown faction {faction} for leader {ldr_name}")
        continue
    if faction not in ldrs_by_faction:
        ldrs_by_faction[faction] = []
    ldr_to_faction[ldr_name] = faction
    ldrs_by_faction[faction].append(ldr_name)
    ldr_total_plays[ldr_name] = 0
    seen_total[ldr_name] = 0

# Let's start parsing the W-L data
ldr_wl = {} # For each leader, the total win loss tie
faction_wl = {} # For each faction, its win-loss-tie
opp_wl = {} # Win-Loss-Tie by opponent
opp_faction_wl = {} # W-L-Ts each faction
total_wl = [0, 0, 0]
in_lines = in_file.readlines()
in_file.close()
in_lines = [line.strip() for line in in_lines]
for line in in_lines:
    if line == '':
        continue
    line = line.split('//')[0].strip()
    try:
        my_faction, my_ldr, opp_faction, opp_ldr, opp_name, result = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if my_ldr != "Unknown" and my_ldr not in seen_total:
        print(f"My leader not recognized: {my_ldr}")
        continue
    if opp_ldr != "Unknown" and opp_ldr not in seen_total:
        print(f"Opponent's leader not recognized: {opp_ldr}")
        continue
    if result not in ['W', 'L']:
        print("Invalid response in line:")
        print(line)
        continue
    if my_ldr != "Unknown":
        if my_ldr not in ldr_wl:
            ldr_wl[my_ldr] = [0, 0]
        seen_total[my_ldr] += 1
        ldr_total_plays[my_ldr] += 1

    if opp_ldr != "Unknown":
        seen_total[opp_ldr] += 1

    if my_faction not in faction_wl:
        faction_wl[my_faction] = [0, 0]
    if opp_name not in opp_wl:
        opp_wl[opp_name] = [0, 0]
    if opp_faction not in opp_faction_wl:
        opp_faction_wl[opp_faction] = [0, 0]
    if result == 'W':
        total_wl[0] += 1
        if my_ldr != "Unknown":
            ldr_wl[my_ldr][0] += 1
        faction_wl[my_faction][0] += 1
        opp_wl[opp_name][0] += 1
        opp_faction_wl[opp_faction][0] += 1
    elif result == 'L':
        total_wl[1] += 1
        if my_ldr != "Unknown":
            ldr_wl[my_ldr][1] += 1
        faction_wl[my_faction][1] += 1
        opp_wl[opp_name][1] += 1
        opp_faction_wl[opp_faction][1] += 1

double_print(f"My current record (W-L) is {total_wl[0]}-{total_wl[1]}", out_file_h)

double_print(f"\nMy record by leader: ({len(seen_total)} total leader in game)", out_file_h)
ldr_play_tuples = []
for faction, faction_ids in sorted(ldrs_by_faction.items()):
    faction_wl_str = f"{faction}:"
    if faction in faction_wl:
        faction_wl_str = f"{faction}: {faction_wl[faction][0]}-{faction_wl[faction][1]}"
    double_print(faction_wl_str, out_file_h)
    for ldr_name in faction_ids:
        if ldr_name in ldr_wl:
            ldr_play_tuples.append((ldr_name, sum(ldr_wl[ldr_name])))
            out_str = f" - {ldr_name}: {ldr_wl[ldr_name][0]}-{ldr_wl[ldr_name][1]}"
            double_print(out_str, out_file_h)

ldr_play_tuples = sorted(ldr_play_tuples, key=lambda x: (-1 * x[1], x[0]))
double_print(f"\nMy H-Index is {get_h_index(ldr_play_tuples)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent, this_opp_wl in sorted(opp_wl.items()):
    opp_wl_str = f"- {opponent}: {this_opp_wl[0]}-{this_opp_wl[1]}"
    double_print(opp_wl_str, out_file_h)

double_print("\nMy record against opposing factions:", out_file_h)
for opp_faction, faction_wl in sorted(opp_faction_wl.items()):
    faction_wl_str = f"- {opp_faction}: {faction_wl[0]}-{faction_wl[1]}"
    double_print(faction_wl_str, out_file_h)

# Least seen leader
LEAST_PLAYED_QTY = 100
least_played_ids = []
for ldr_name, id_played in seen_total.items():
    if id_played < LEAST_PLAYED_QTY:
        LEAST_PLAYED_QTY = id_played
        least_played_ids = [ldr_name]
    elif id_played == LEAST_PLAYED_QTY:
        least_played_ids.append(ldr_name)

double_print("\nI've seen the following leaders on the table the least " + \
        f"({LEAST_PLAYED_QTY} times)", out_file_h)
double_print("; ".join(sorted(least_played_ids)), out_file_h)

# Figure out least played relevant leader
faction_plays = {}
filtered_ldr_plays = []
for check_id, ldr_plays in ldr_total_plays.items():
    this_faction = ldr_to_faction[check_id]
    filtered_ldr_plays.append((check_id, ldr_plays))
    if this_faction not in faction_plays:
        faction_plays[this_faction] = 0
    faction_plays[this_faction] += ldr_plays
faction_play_sorter = []
for this_faction, faction_plays in faction_plays.items():
    faction_play_sorter.append((this_faction, faction_plays))
faction_play_sorter = sorted(faction_play_sorter, key=lambda x:(x[1], x[0]))

LOWEST_FLEET = faction_play_sorter[0]
relevant_ldr_plays = []

for ldr_name, ldr_plays in filtered_ldr_plays:
    if ldr_to_faction[ldr_name] == LOWEST_FLEET[0]:
        relevant_ldr_plays.append((ldr_name, ldr_plays))
relevant_ldr_plays = sorted(relevant_ldr_plays, key=lambda x:(x[1], x[0]))

low_ldr = relevant_ldr_plays[0]
LOW_O_STR = f"\nI should play more games with {LOWEST_FLEET[0]}, where I only have " + \
    f"{int(LOWEST_FLEET[1])} games. Suggested leader - {low_ldr[0]} ({low_ldr[1]} " + \
    "total plays)"
double_print(LOW_O_STR, out_file_h)
