#!/usr/bin/python3

"""
Tracker and army suggestion tool for games of One Piece
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.get_h_index import get_h_index

if os.getcwd().endswith('card_games'):
    out_file_h = open("wl_output/OnePieceWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('wl_data/OnePieceResults.txt', 'r', encoding="UTF-8")
    source_data_file = open('DB/OnePieceData.txt', 'r', encoding="UTF-8")
else:
    out_file_h = open("card_games/wl_output/OnePieceWLOut.txt", 'w', encoding="UTF-8")
    in_file = open('card_games/wl_data/OnePieceResults.txt', 'r', encoding="UTF-8")
    source_data_file = open('card_games/DB/OnePieceData.txt', 'r', encoding="UTF-8")

double_print("One Piece Win-Loss Tracker and deck selector\n", out_file_h)

BANNED_LEADERS = ['Trafalgar Law (ST10-001)', 'Sakazuki (OP05-041)']
color_map = {'P':'Purple', 'B':'Black', 'R':'Red', 'Y':'Yellow', 'U':'Blue', 'G':'Green'}

data_lines = in_file.readlines()
in_file.close()
data_lines = [line.strip() for line in data_lines]

source_data_lines = source_data_file.readlines()
source_data_file.close()
source_data_lines = [line.strip() for line in source_data_lines]
leader_games_map = {} # Total number of games I've seen the leader
for line in source_data_lines:
    if line.startswith('#') or line.strip() == '':
        continue
    if line.split(';')[2] == 'Leader':
        leader_name = line.split(';')[0]
        leader_num = line.split(';')[1]
        colors = []
        for color in line.split(';')[3].split('/'):
            colors.append(color_map[color])
        leader_games_map[f"{leader_name} ({leader_num})"] = 0

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

    my_leader = f"{my_leader} ({card_number})"
    opp_leader = f"{opp_leader} ({opp_leader_card_num})"
    if my_leader not in leader_games_map:
        double_print(f"Invalid leader: {my_leader}", out_file_h)
    if opp_leader not in leader_games_map:
        double_print(f"Invalid leader: {opp_leader}", out_file_h)

    leader_games_map[my_leader] += 1
    leader_games_map[opp_leader] += 1

    if w_l not in ['W', 'L']:
        double_print(f"Invalid W/L: {w_l}", out_file_h)

    if my_leader not in my_leader_wl:
        my_leader_wl[my_leader] = [0, 0]
    if opponent not in my_opp_wl:
        my_opp_wl[opponent] = [0, 0]
    if opp_leader not in my_opp_leader_wl:
        my_opp_leader_wl[opp_leader] = [0, 0]

    if w_l == 'W':
        my_leader_wl[my_leader][0] += 1
        my_opp_wl[opponent][0] += 1
        total_wl[0] += 1
        my_opp_leader_wl[opp_leader][0] += 1
    if w_l == 'L':
        my_leader_wl[my_leader][1] += 1
        my_opp_wl[opponent][1] += 1
        total_wl[1] += 1
        my_opp_leader_wl[opp_leader][1] += 1

double_print(f"My current record is {total_wl[0]}-{total_wl[1]}\n", out_file_h)
double_print("My record by leader:", out_file_h)
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
    if leader in BANNED_LEADERS:
        continue
    if leader_games < MIN_SEEN:
        MIN_SEEN = leader_games
        min_seen_leaders = [leader]
    elif leader_games == MIN_SEEN:
        min_seen_leaders.append(leader)
double_print(f"\nI've seen these leaders on the table the least ({MIN_SEEN} times): " + \
    f"{'; '.join(sorted(min_seen_leaders))}", out_file_h)

playable_leader_list = []
for leader in leader_games_map:
    if leader in BANNED_LEADERS:
        continue
    if leader not in my_leader_wl:
        playable_leader_list.append((leader, 0))
    else:
        playable_leader_list.append((leader, sum(my_leader_wl[leader])))
playable_leader_list = sorted(playable_leader_list, key=lambda x:(x[1], x[0]))
least_leader = playable_leader_list[0][0]
least_leader_games = playable_leader_list[0][1]

sugg_string = f"\nI should play more games with {least_leader}, as I only have " + \
    f"{least_leader_games} game{('', 's')[least_leader_games != 1]}"
double_print(sugg_string, out_file_h)
