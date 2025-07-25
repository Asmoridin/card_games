#!/usr/bin/python3

"""
Summarizes the current collection status of all tracked card/dice games
"""

import os
import importlib.util
import sys

from steve_utils.output_utils import double_print

from card_games.list_scripts import wyvern
from card_games.list_scripts import lorcana
from card_games.list_scripts import one_piece
from card_games.list_scripts import grand_archive
from card_games.list_scripts import star_trek_second_edition
from card_games.list_scripts import star_trek_first_edition
from card_games.list_scripts import star_wars_unlimited
from card_games.list_scripts import tribbles
from card_games.list_scripts import wars_tcg
from card_games.list_scripts import xena
from card_games.list_scripts import star_wars_ccg

modules = [
    ("card_games/A/Anachronism/anachronism.py", "anachronism"),
    ("card_games/City_of_Heroes/city_of_heroes.py", "city_of_heroes"),
    ("card_games/D/Daemon_Dice/daemon_dice.py", "daemon_dice"),
    ("card_games/D/Dragon_Dice/dragon_dice.py", "dragon_dice"),
    ("card_games/D/DBS_Fusion_World/dbs_fusion_world.py", "dbs_fusion_world"),
    ("card_games/Legend_of_the_Five_Rings/l5r.py", "l5r"),
    ("card_games/Magic_the_Gathering/magic_gathering.py", "magic_gathering"),
    ("card_games/Star_Wars_LCG/star_wars_lcg.py", "star_wars_lcg"),
]

added_modules = []
for file_path, module_name in modules:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    MY_MODULE = None
    if spec:
        MY_MODULE = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = MY_MODULE  # Optional: add to sys.modules
        spec.loader.exec_module(MY_MODULE)
        added_modules.append(MY_MODULE)
    else:
        print(f"Could not find module at {file_path}")

if os.getcwd().endswith('card_games'):
    in_file = open("DB/NewCardGames.txt", encoding="UTF-8")
    mag_file = open("DB/Magazines.txt", encoding="UTF-8")
else:
    in_file = open("card_games/DB/NewCardGames.txt", encoding="UTF-8")
    mag_file = open("card_games/DB/Magazines.txt", encoding="UTF-8")

#print("\033[96mTest.\033[0m")

started_games = [star_wars_unlimited,
    star_trek_second_edition, tribbles, wyvern, grand_archive,
    lorcana, one_piece, star_trek_first_edition, wars_tcg, xena,
    star_wars_ccg]
started_games.extend(added_modules)

TOTAL_HAVE = 0
TOTAL_MAX = 0
NEW_GAMES_STARTED = 1 + len(started_games)
game_data = []

# Add Magazine info
mag_lines = mag_file.readlines()
mag_file.close()
mag_lines = [line.strip() for line in mag_lines]
magazine_max = {"Inquest": 150, 'Scrye': 131}
magazine_have = {"Inquest": 0, 'Scrye':0}
for mag_line in mag_lines:
    mag_line_vals = mag_line.split(';')
    if mag_line_vals[0] in magazine_have:
        magazine_have[mag_line_vals[0]] += 1
for mag_name, mag_own in magazine_have.items():
    game_data.append((mag_name, mag_own, magazine_max[mag_name]))
    TOTAL_HAVE += mag_own
    TOTAL_MAX += magazine_max[mag_name]

NEW_GAMES_STARTED = 1 + len(started_games) + len(magazine_max)

other_games = in_file.readlines()
in_file.close()
other_games = [line.strip() for line in other_games]

new_games_count = len(other_games) + NEW_GAMES_STARTED

for game in started_games:
    TOTAL_HAVE += game.TOTAL_OWN
    TOTAL_MAX += game.TOTAL_MAX
    game_data.append((game.GAME_NAME, game.TOTAL_OWN, game.TOTAL_MAX))

game_data.append(("New Game", NEW_GAMES_STARTED + 1, new_games_count + 1))
game_data = sorted(game_data, key=lambda x:(x[1]/x[2], -1 * (x[2] - x[1])))
largest_collection = sorted(game_data, key=lambda x:x[1], reverse = True)

if __name__ == "__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("output/CCGSummaryOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/output/CCGSummaryOut.txt", 'w', encoding="UTF-8")
    total_percentage = TOTAL_HAVE * 100 /TOTAL_MAX
    total_string = f"Totaling {len(game_data) - 1} games, owning {TOTAL_HAVE} out of " + \
        f"{TOTAL_MAX} cards/dice ({total_percentage:.2f} percent)"
    double_print(total_string, out_file_h)
    lowest_game_percentage = game_data[0][1]*100/game_data[0][2]
    lowest_game_string = f"Lowest game is {game_data[0][0]} at {lowest_game_percentage:.2f} " + \
        f"percent ({game_data[0][1]} / {game_data[0][2]})"
    double_print(lowest_game_string, out_file_h)

    double_print("\nFive Lowest Games (by percentage):", out_file_h)
    for game_info in game_data[:5]:
        info_n, info_h, info_t = game_info
        info_p = info_h/info_t
        pt_str = f"- {info_n}: {100 * info_p:.2f} ({info_h}/{info_t})"
        double_print(pt_str, out_file_h)

    double_print("\nLargest Collections:", out_file_h)
    for game_info in largest_collection[:5]:
        info_n, info_h, _  = game_info
        PT_STR = f"- {info_n}: {info_h}"
        double_print(PT_STR, out_file_h)

    out_file_h.close()
