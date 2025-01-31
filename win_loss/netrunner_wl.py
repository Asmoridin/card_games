#!/usr/bin/python3

"""
Win-Loss tracker and ID suggestion tool for Android: Netrunner
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index

if os.getcwd().endswith('card_games'):
    out_file_h = open("wl_output/NetrunnerOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/AndroidNetrunnerWL.txt', 'r', encoding="UTF-8")
    id_data_file = open('wl_data/NetrunnerIDs.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("card_games/wl_output/NetrunnerOut.txt", 'w', encoding="UTF-8")
    in_file = open('card_games/wl_data/AndroidNetrunnerWL.txt', 'r', encoding="UTF-8")
    id_data_file = open('card_games/wl_data/NetrunnerIDs.txt', 'r', encoding="UTF-8")

CURRENT_FORMAT = "Standard"

double_print("Android: Netrunner Win-Loss Tracker, and deck selector", out_file_h)

CORP_FACTIONS = ['Weyland', 'Haas-Bioroid', 'NBN', 'Jinteki', 'Neutral Corp']
RUNNER_FACTIONS = ['Neutral Runner', 'Shaper', 'Anarch', 'Criminal']

# Let's read the IDs, and parse the ID data
identities = {'Startup':{}, 'Standard':{}, 'Extended':{}}
id_by_faction = {}
id_to_faction = {}
id_total_plays = {}
seen_total = {}
id_lines = id_data_file.readlines()
id_data_file.close()
id_lines = [line.strip() for line in id_lines]
for id_line in id_lines:
    identity_name, ID_FACTION, id_format = id_line.split(';')
    if ID_FACTION == 'HB':
        ID_FACTION = 'Haas-Bioroid'
    if ID_FACTION not in CORP_FACTIONS and ID_FACTION not in RUNNER_FACTIONS:
        print(f"Unknown faction {ID_FACTION} for ID {identity_name}")
        continue
    if id_format not in ['Standard', 'Extended', 'Startup']:
        print(f"Unknown format {id_format} for ID {identity_name}")
        continue
    if ID_FACTION not in id_by_faction:
        id_by_faction[ID_FACTION] = []
    id_by_faction[ID_FACTION].append(identity_name)
    id_to_faction[identity_name] = ID_FACTION
    id_total_plays[identity_name] = 0
    seen_total[identity_name] = 0
    do_formats = ['Extended']
    if id_format in ['Standard', 'Startup']:
        do_formats.append('Standard')
    if id_format == 'Startup':
        do_formats.append('Startup')
    for do_format in do_formats:
        if ID_FACTION not in identities[do_format]:
            identities[do_format][ID_FACTION] = []
        identities[do_format][ID_FACTION].append(identity_name)

# Let's start parsing the W-L data
id_wl = {} # For each ID, the total win loss
faction_wl = {} # For each faction, it's win-loss
opp_wl = {} # Win-Loss by opponent
opp_faction_wl = {} # W-L against each faction
total_wl = [0, 0]
corp_wl = [0, 0]
runner_wl = [0, 0]
in_lines = in_file.readlines()
in_file.close()
in_lines = [line.strip() for line in in_lines]
for line in in_lines:
    if line == '':
        continue
    try:
        my_id, opp_id, opp_name, result = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if my_id not in id_to_faction:
        print(f"My ID not recognized: {my_id}")
        continue
    if opp_id not in id_to_faction:
        print(f"Opponent's ID not recognized: {opp_id}")
        continue
    my_faction = id_to_faction[my_id]
    opp_faction = id_to_faction[opp_id]
    if result not in ['W', 'L']:
        print("Invalid response in line:")
        print(line)
        continue
    if my_id not in id_wl:
        id_wl[my_id] = [0, 0]
    seen_total[my_id] += 1
    seen_total[opp_id] += 1
    if my_faction not in faction_wl:
        faction_wl[my_faction] = [0, 0]
    if opp_name not in opp_wl:
        opp_wl[opp_name] = [0, 0]
    if opp_faction not in opp_faction_wl:
        opp_faction_wl[opp_faction] = [0, 0]
    if result == 'W':
        total_wl[0] += 1
        id_wl[my_id][0] += 1
        faction_wl[my_faction][0] += 1
        opp_wl[opp_name][0] += 1
        opp_faction_wl[opp_faction][0] += 1
        id_total_plays[my_id] += 1
        if my_faction in CORP_FACTIONS:
            corp_wl[0] += 1
        else:
            runner_wl[0] += 1
    if result == 'L':
        total_wl[1] += 1
        id_wl[my_id][1] += 1
        faction_wl[my_faction][1] += 1
        opp_wl[opp_name][1] += 1
        opp_faction_wl[opp_faction][1] += 1
        id_total_plays[my_id] += 1
        if my_faction in CORP_FACTIONS:
            corp_wl[1] += 1
        else:
            runner_wl[1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)

double_print(f"Record as Corporation: {corp_wl[0]}-{corp_wl[1]}", out_file_h)
double_print(f"Record as Runner: {runner_wl[0]}-{runner_wl[1]}", out_file_h)

double_print("\nMy record by identity:", out_file_h)
for faction, faction_ids in sorted(id_by_faction.items()):
    faction_wl_str = f"{faction}:"
    if faction in faction_wl:
        faction_wl_str = f"{faction}: {faction_wl[faction][0]}-{faction_wl[faction][1]}"
    double_print(faction_wl_str, out_file_h)
    for id_name in faction_ids:
        if id_name in id_wl:
            double_print(f" - {id_name}: {id_wl[id_name][0]}-{id_wl[id_name][1]}", out_file_h)

corp_h_index = []
runner_h_index = []
for faction, faction_ids in sorted(id_by_faction.items()):
    for id_name in faction_ids:
        if id_name in id_wl:
            if faction in CORP_FACTIONS:
                corp_h_index.append((id_name, sum(id_wl[id_name])))
            else:
                runner_h_index.append((id_name, sum(id_wl[id_name])))

corp_h_index = sorted(corp_h_index, key=lambda x:x[1], reverse=True)
double_print(f"\nCorp H-Index is {get_h_index(corp_h_index)}", out_file_h)
runner_h_index = sorted(runner_h_index, key=lambda x:x[1], reverse=True)
double_print(f"Runner H-Index is {get_h_index(runner_h_index)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent, this_opp_wl in sorted(opp_wl.items()):
    opp_wl_str = f"- {opponent}: {this_opp_wl[0]}-{this_opp_wl[1]}"
    double_print(opp_wl_str, out_file_h)

double_print("\nMy record against opposing factions:", out_file_h)
for opp_faction, fac_wl in sorted(opp_faction_wl.items()):
    faction_wl_str = f"- {opp_faction}: {fac_wl[0]}-{fac_wl[1]}"
    double_print(faction_wl_str, out_file_h)

# Least seen IDs
LEAST_PLAYED_QTY = 100
least_played_ids = []
for id_name, id_played in seen_total.items():
    if id_played < LEAST_PLAYED_QTY:
        LEAST_PLAYED_QTY = id_played
        least_played_ids = [id_name]
    elif id_played == LEAST_PLAYED_QTY:
        least_played_ids.append(id_name)

double_print(f"\nI've seen the following IDs on the table the least ({LEAST_PLAYED_QTY} times)",
    out_file_h)
double_print(", ".join(least_played_ids), out_file_h)

# Figure out least played relevant ID
CORP_WEIGHT = len(identities[CURRENT_FORMAT]['Weyland']) + \
    len(identities[CURRENT_FORMAT]['Haas-Bioroid'])+ len(identities[CURRENT_FORMAT]['NBN']) + \
    len(identities[CURRENT_FORMAT]['Jinteki'])
CORP_WEIGHT = CORP_WEIGHT / 4
CORP_WEIGHT = CORP_WEIGHT / len(identities[CURRENT_FORMAT]['Neutral Corp'])
RUNNER_WEIGHT = len(identities[CURRENT_FORMAT]['Anarch']) + \
    len(identities[CURRENT_FORMAT]['Shaper']) + len(identities[CURRENT_FORMAT]['Criminal'])
RUNNER_WEIGHT = RUNNER_WEIGHT / 3
RUNNER_WEIGHT = RUNNER_WEIGHT / len(identities[CURRENT_FORMAT]['Neutral Runner'])

faction_plays = {}
filtered_id_plays = []
for check_id, id_plays in id_total_plays.items():
    this_faction = id_to_faction[check_id]
    if check_id in identities[CURRENT_FORMAT][this_faction]:
        filtered_id_plays.append((check_id, id_plays))
        if this_faction not in faction_plays:
            faction_plays[this_faction] = 0
        faction_plays[this_faction] += id_plays
fac_play_sorter = []
for this_fac, fac_plays in faction_plays.items():
    if this_fac == "Neutral Runner":
        fac_plays *= RUNNER_WEIGHT
    if this_fac == "Neutral Corp":
        fac_plays *= CORP_WEIGHT
    fac_play_sorter.append((this_fac, fac_plays))
fac_play_sorter = sorted(fac_play_sorter, key=lambda x:(x[1], x[0]))

LOWEST_CORP = None
LOWEST_RUNNER = None
for faction, faction_plays in fac_play_sorter:
    if LOWEST_CORP is None and faction in CORP_FACTIONS:
        LOWEST_CORP = (faction, faction_plays)
    if LOWEST_RUNNER is None and faction in RUNNER_FACTIONS:
        LOWEST_RUNNER = (faction, faction_plays)

corp_id_plays = []
runner_id_plays = []
for id_name, id_plays in filtered_id_plays:
    if id_to_faction[id_name] == LOWEST_CORP[0]:
        corp_id_plays.append((id_name, id_plays))
    if id_to_faction[id_name] in LOWEST_RUNNER[0]:
        runner_id_plays.append((id_name, id_plays))

corp_id_plays = sorted(corp_id_plays, key=lambda x:(x[1], x[0]))
runner_id_plays = sorted(runner_id_plays, key=lambda x:(x[1], x[0]))

double_print(f"\nFollowing are limited to my current format ({CURRENT_FORMAT})", out_file_h)
WEIGHT_STR = ""
low_c_id = corp_id_plays[0]
if LOWEST_CORP[0] == "Neutral Corp":
    WEIGHT_STR = " (weighted)"
LOW_C_STR = f"I should play more games with {LOWEST_CORP[0]}, where I only have " + \
    f"{int(LOWEST_CORP[1])}{WEIGHT_STR} games. Suggested ID - {low_c_id[0]} ({low_c_id[1]} " + \
    "total plays)"
double_print(LOW_C_STR, out_file_h)

WEIGHT_STR = ""
low_r_id = runner_id_plays[0]
if LOWEST_RUNNER[0] == "Neutral Runner":
    WEIGHT_STR = " (weighted)"
LOW_R_STR = f"I should play more games with {LOWEST_RUNNER[0]}, where I only have " + \
    f"{int(LOWEST_RUNNER[1])}{WEIGHT_STR} games. Suggested ID - {low_r_id[0]} ({low_r_id[1]} " + \
    "total plays)"
double_print(LOW_R_STR, out_file_h)
