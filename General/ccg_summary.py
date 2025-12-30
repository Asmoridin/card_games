#!/usr/bin/python3

"""
Summarizes the current collection status of all tracked card/dice games
"""

import os
import importlib.util
import sys

from card_games.General.Libraries.output_utils import double_print

modules = [
    ("card_games/A/Anachronism/anachronism.py", "anachronism"),
    ("card_games/C/City_of_Heroes/city_of_heroes.py", "city_of_heroes"),
    ("card_games/D/Daemon_Dice/daemon_dice.py", "daemon_dice"),
    ("card_games/D/Dragon_Dice/dragon_dice.py", "dragon_dice"),
    ("card_games/D/DBS_Fusion_World/dbs_fusion_world.py", "dbs_fusion_world"),
    ("card_games/G/Grand_Archive/grand_archive.py", "grand_archive"),
    ("card_games/G/Gundam_Card_Game/gundam_card_game.py", "gundam_card_game"),
    ("card_games/L/Legend_of_the_Five_Rings/l5r.py", "l5r"),
    ("card_games/L/Lorcana/lorcana.py", "lorcana"),
    ("card_games/M/Magic_the_Gathering/magic_gathering.py", "magic_gathering"),
    ("card_games/O/One_Piece_TCG/one_piece_tcg.py", "one_piece_tcg"),
    ("card_games/R/Riftbound/riftbound.py", "riftbound"),
    ("card_games/S/Star_Trek_1E/star_trek_first_edition.py", "star_trek_first_edition"),
    ("card_games/S/Star_Trek_2E/star_trek_second_edition.py", "star_trek_second_edition"),
    ("card_games/S/Star_Wars_CCG/star_wars_ccg.py", "star_wars_ccg"),
    ("card_games/S/Star_Wars_LCG/star_wars_lcg.py", "star_wars_lcg"),
    ("card_games/S/Star_Wars_Unlimited/star_wars_unlimited.py", "star_wars_unlimited"),
    ("card_games/T/Tribbles/tribbles.py", "tribbles"),
    ("card_games/U/Union_Arena/union_arena.py", "union_arena"),
    ("card_games/W/Wars_TCG/wars_tcg.py", "wars_tcg"),
    ("card_games/W/Wheel_of_Time_CCG/wheel_of_time.py", "wheel_of_time"),
    ("card_games/W/Wyvern/wyvern.py", "wyvern"),
    ("card_games/X/Xena_Warrior_Princess/xena.py", "xena"),
]

added_modules = []
for file_path, module_name in modules:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    MY_MODULE = None
    if spec:
        MY_MODULE = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = MY_MODULE  # Optional: add to sys.modules
        if spec.loader is not None:
            spec.loader.exec_module(MY_MODULE)
        added_modules.append(MY_MODULE)
    else:
        print(f"Could not find module at {file_path}")

FILE_PREFIX = "card_games/General"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "General"
in_file = open(FILE_PREFIX + "/Data/NewCardGames.txt", encoding="UTF-8")
mag_file = open(FILE_PREFIX + "/Data/Magazines.txt", encoding="UTF-8")

#print("\033[96mTest.\033[0m")

started_games = []
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
        out_file_h = open("General/CCGSummaryOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/General/CCGSummaryOut.txt", 'w', encoding="UTF-8")
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
    for game_info in largest_collection[:10]:
        info_n, info_h, _  = game_info
        PT_STR = f"- {info_n}: {info_h}"
        double_print(PT_STR, out_file_h)

    out_file_h.close()
