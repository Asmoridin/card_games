#!/usr/bin/python3

"""
Tracker and army suggestion tool for games of DBS: Fusion World
"""

import os

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.get_h_index import get_h_index

FILE_PREFIX = "card_games/D/DBS_Fusion_World"

if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "D/DBS_Fusion_World"

out_file_h = open(FILE_PREFIX + "/DBSFWOut.txt", 'w', encoding="UTF-8")
in_file = open(FILE_PREFIX + '/Data/DBSFW-Results.txt', 'r', encoding="UTF-8")
source_data_file = open(FILE_PREFIX + '/Data/DBSCGFusionWorld.txt', 'r', encoding="UTF-8")

double_print("DBS: Fusion World Win-Loss Tracker and deck selector\n", out_file_h)

data_lines = in_file.readlines()
in_file.close()
data_lines = [line.strip() for line in data_lines]

source_data_lines = source_data_file.readlines()
source_data_file.close()
source_data_lines = [line.strip() for line in source_data_lines]
leader_games_map = {} # Total number of games I've seen the leader
leader_color_map = {}
for line in source_data_lines:
    if line.startswith('#') or line.strip() == '':
        continue
    if line.split(';')[2] == 'Leader':
        leader_name = line.split(';')[0]
        leader_num = line.split(';')[5]
        colors = []
        for color in line.split(';')[3].split('/'):
            colors.append(color)
        leader_games_map[f"{leader_name} ({leader_num})"] = 0
        leader_color_map[f"{leader_name} ({leader_num})"] = colors

my_leader_wl = {}
my_opp_wl = {}
my_opp_leader_wl = {}
total_wl = [0, 0]

for line in data_lines:
    if line == "":
        continue
    if line.startswith('#'):
        continue
    my_leader, card_number, opp_leader, opp_leader_card_num, opponent, w_l = line.split(';')

    MY_LEADER_STR = f"{my_leader} ({card_number})"
    OPP_LEADER_STR = f"{opp_leader} ({opp_leader_card_num})"
    if MY_LEADER_STR not in leader_games_map:
        double_print(f"Invalid leader: {MY_LEADER_STR}", out_file_h)
    if OPP_LEADER_STR not in leader_games_map:
        double_print(f"Invalid leader: {OPP_LEADER_STR}", out_file_h)

    leader_games_map[MY_LEADER_STR] += 1
    leader_games_map[OPP_LEADER_STR] += 1

    if w_l not in ['W', 'L']:
        double_print(f"Invalid W/L: {w_l}", out_file_h)

    if MY_LEADER_STR not in my_leader_wl:
        my_leader_wl[MY_LEADER_STR] = [0, 0]
    if opponent not in my_opp_wl:
        my_opp_wl[opponent] = [0, 0]
    if OPP_LEADER_STR not in my_opp_leader_wl:
        my_opp_leader_wl[OPP_LEADER_STR] = [0, 0]

    if w_l == 'W':
        my_leader_wl[MY_LEADER_STR][0] += 1
        my_opp_wl[opponent][0] += 1
        total_wl[0] += 1
        my_opp_leader_wl[OPP_LEADER_STR][0] += 1
    if w_l == 'L':
        my_leader_wl[MY_LEADER_STR][1] += 1
        my_opp_wl[opponent][1] += 1
        total_wl[1] += 1
        my_opp_leader_wl[OPP_LEADER_STR][1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
LDR_SUM= f"My record by leader: (I have played {len(my_leader_wl)} out of {len(leader_games_map)})"
double_print(LDR_SUM, out_file_h)
for leader in sorted(my_leader_wl):
    double_print(f"{leader}: {my_leader_wl[leader][0]}-{my_leader_wl[leader][1]}", out_file_h)

leader_h_index = []
for leader, l_w_l in my_leader_wl.items():
    leader_h_index.append((leader, sum(l_w_l)))
leader_h_index = sorted(leader_h_index, key=lambda x:x[1], reverse=True)

double_print(f"\nMy H-Index is {get_h_index(leader_h_index)}", out_file_h)

double_print("\nMy record against opponents:", out_file_h)
for opponent in sorted(my_opp_wl):
    double_print(f"{opponent}: {my_opp_wl[opponent][0]}-{my_opp_wl[opponent][1]}", out_file_h)

double_print("\nMy record against opposing leaders:", out_file_h)
for opp_leader in sorted(my_opp_leader_wl):
    ldr_str = f"{opp_leader}: {my_opp_leader_wl[opp_leader][0]}-{my_opp_leader_wl[opp_leader][1]}"
    double_print(ldr_str, out_file_h)

MIN_SEEN = 1000000
min_seen_leaders = []
for leader, leader_games in leader_games_map.items():
    if leader_games < MIN_SEEN:
        MIN_SEEN = leader_games
        min_seen_leaders = [leader]
    elif leader_games == MIN_SEEN:
        min_seen_leaders.append(leader)
double_print(f"\nI've seen these leaders on the table the least ({MIN_SEEN} times): " + \
    f"{'; '.join(sorted(min_seen_leaders))}", out_file_h)

playable_leader_list = []
for leader in leader_games_map:
    if leader not in my_leader_wl:
        playable_leader_list.append((leader, 0))
    else:
        playable_leader_list.append((leader, sum(my_leader_wl[leader])))
playable_leader_list = sorted(playable_leader_list, key=lambda x:(x[1], x[0]))
printed_colors = set()

double_print("\nLeast played leaders by color:", out_file_h)
for check_leader in playable_leader_list:
    this_ldr_color = leader_color_map[check_leader[0]]
    if set(this_ldr_color).intersection(printed_colors) == set([]):
        color_str = f"- {check_leader[0]}: {check_leader[1]} games ({'/'.join(this_ldr_color)})"
        double_print(color_str, out_file_h)
        printed_colors = printed_colors.union(set(this_ldr_color))
