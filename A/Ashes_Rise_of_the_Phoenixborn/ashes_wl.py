#!/usr/bin/python3

"""
Tracker and army suggestion tool for games of Ashes: Rise of the Phoenixborn
"""

import os

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.get_h_index import get_h_index

FILE_PREFIX = "card_games/A/Ashes_Rise_of_the_Phoenixborn"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "A/Ashes_Rise_of_the_Phoenixborn"

out_file_h = open(FILE_PREFIX + "/AshesOut.txt", 'w', encoding="UTF-8")

all_phoenixborn = ['Aradel Summergaard', 'Astrea', 'Brennen Blackcloud', 'Coal Roarkwin',
    'Dimona Odinstar', 'Echo Greystorm', 'Fiona Mercywind', 'Harold Westraven', 'Hope Everthorn',
    'James Endersight', 'Jericho, Reborn', 'Jessa Na Ni', 'Koji Wolfcub', 'Leo Sunshadow',
    'Lulu Firststone', 'Maeoni Viper', 'Namine Hymntide', 'Noah Redmoon', 'Odette Diamondcrest',
    'Orrick Gilstream', 'Rimea Careworn', 'Rin Northfell', 'Rowan Umberend', 'Saria Guideman',
    'Sembali Grimtongue', 'Tristan Darkwater', 'Victoria Glassfire', 'Xander Heartsblood',
    'Jerico Kill', 'Arren Frostpeak', 'Issa Brightmore',
]

double_print("Ashes: Rise of the Phoenixborn Win-Loss Tracker and deck selector", out_file_h)

with open(FILE_PREFIX + '/Data/AshesWL.txt', 'r', encoding="UTF-8") as in_file:
    data_lines = in_file.readlines()
data_lines = [line.strip() for line in data_lines]

my_pb_wl = {}
my_opp_wl = {}
my_opp_pb_wl = {}
total_wl = [0, 0]
pb_games_map = {}
for pb in all_phoenixborn:
    pb_games_map[pb] = 0

for line in data_lines:
    if line == "":
        continue
    if line.startswith('#'):
        continue
    my_pb, opp_pb, opponent, w_l = line.split(';')

    if my_pb not in all_phoenixborn:
        double_print(f"Invalid Phoenixborn: {my_pb}", out_file_h)
        continue
    if opp_pb not in all_phoenixborn:
        double_print(f"Invalid Phoenixborn: {opp_pb}", out_file_h)
        continue

    pb_games_map[my_pb] += 1
    pb_games_map[opp_pb] += 1

    if w_l not in ['W', 'L']:
        double_print(f"Invalid W/L: {w_l}", out_file_h)

    if my_pb not in my_pb_wl:
        my_pb_wl[my_pb] = [0, 0]
    if opponent not in my_opp_wl:
        my_opp_wl[opponent] = [0, 0]
    if opp_pb not in my_opp_pb_wl:
        my_opp_pb_wl[opp_pb] = [0, 0]

    if w_l == 'W':
        my_pb_wl[my_pb][0] += 1
        my_opp_wl[opponent][0] += 1
        total_wl[0] += 1
        my_opp_pb_wl[opp_pb][0] += 1
    if w_l == 'L':
        my_pb_wl[my_pb][1] += 1
        my_opp_wl[opponent][1] += 1
        total_wl[1] += 1
        my_opp_pb_wl[opp_pb][1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
double_print(f"My record by phoenixborn ({len(all_phoenixborn)} total phoenixborn):", out_file_h)
for pb in sorted(my_pb_wl):
    double_print(f"{pb}: {my_pb_wl[pb][0]}-{my_pb_wl[pb][1]}", out_file_h)

pb_h_index = []
for pb, l_w_l in my_pb_wl.items():
    pb_h_index.append((pb, sum(l_w_l)))
pb_h_index = sorted(pb_h_index, key=lambda x:x[1], reverse=True)

double_print(f"\nMy H-Index is {get_h_index(pb_h_index)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent in sorted(my_opp_wl):
    double_print(f"{opponent}: {my_opp_wl[opponent][0]}-{my_opp_wl[opponent][1]}", out_file_h)

double_print("\nMy record against opposing phoenixborn:", out_file_h)
for opp_pb in sorted(my_opp_pb_wl):
    OPP_PBORN_STR = f"{opp_pb}: {my_opp_pb_wl[opp_pb][0]}-{my_opp_pb_wl[opp_pb][1]}"
    double_print(OPP_PBORN_STR, out_file_h)

MIN_SEEN = 1000000
min_seen_pbs = []
for pb, pb_games in pb_games_map.items():
    if pb_games < MIN_SEEN:
        MIN_SEEN = pb_games
        min_seen_pbs = [pb]
    elif pb_games == MIN_SEEN:
        min_seen_pbs.append(pb)
double_print(f"\nI've seen these phoenixborn on the table the least ({MIN_SEEN} times): " + \
    f"{'; '.join(sorted(min_seen_pbs))}", out_file_h)

playable_pb_list = []
for pb in all_phoenixborn:
    if pb not in my_pb_wl:
        playable_pb_list.append((pb, 0))
    else:
        playable_pb_list.append((pb, sum(my_pb_wl[pb])))
playable_pb_list = sorted(playable_pb_list, key=lambda x:(x[1], x[0]))
least_pb = playable_pb_list[0][0]
least_pb_games = playable_pb_list[0][1]

PB_SUGG_STR = f"\nI should play more games with {least_pb}, as I only have " + \
    f"{least_pb_games} game{('', 's')[least_pb_games != 1]}"
double_print(PB_SUGG_STR, out_file_h)
