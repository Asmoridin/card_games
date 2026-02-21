#!/usr/bin/python3

"""
Summarizes the current collection status of all tracked card/dice games
"""

import os
import importlib.util
import math
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
    ("card_games/P/Pokemon/pokemon.py", "pokemon"),
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

# Process Play Data

PLAY_DIR = os.path.join(FILE_PREFIX, "Data", "Plays")

# Fix for renamed games
GAME_NAME_FIX = {
    "Hordes: High Command": "Warmachine: High Command",
    "Shadowfist: Combat In Kowloon": "Shadowfist",
    "Spearpoint 1943: Eastern Front": "Spearpoint 1943",
    "Summoner Wars": "Summoner Wars (Second Edition)",
}

game_plays_total = {}
game_year_counter = {} # To track in how many years a game was playable
YEARS_PROCESSED = 0
prev_year_plays = {}
for play_file in sorted(os.listdir(PLAY_DIR))[:-1]:
    if not play_file.endswith(".txt"):
        continue
    YEARS_PROCESSED += 1
    prev_year_plays = {}
    with open(os.path.join(PLAY_DIR, play_file), encoding="UTF-8") as play_file_h:
        play_lines = play_file_h.readlines()
    play_lines = [line.strip() for line in play_lines]
    this_years_plays = []
    for play_line in play_lines:
        if play_line == "":
            continue
        play_game, play_count = play_line.split(';')
        play_game = play_game.strip()
        if play_game in GAME_NAME_FIX:
            play_game = GAME_NAME_FIX[play_game]
        play_count = int(play_count)
        this_years_plays.append((play_game, play_count))
        if play_game not in game_plays_total:
            game_year_counter[play_game] = 0
            game_plays_total[play_game] = 0
        game_plays_total[play_game] += play_count
        prev_year_plays[play_game] = play_count
    for game_name in game_year_counter:
        game_year_counter[game_name] += 1

    this_years_plays = sorted(this_years_plays, key=lambda x:x[1], reverse=True)

PREV_YEAR_PLAY_TOTAL = 0
for game_name, play_count in prev_year_plays.items():
    PREV_YEAR_PLAY_TOTAL += play_count

# Get current year data
THIS_YEAR_PLAYS = 0
current_year_file = sorted(os.listdir(PLAY_DIR))[-1]
with open(os.path.join(PLAY_DIR, current_year_file), encoding="UTF-8") as play_file_h:
    current_play_lines = play_file_h.readlines()
current_play_lines = [line.strip() for line in current_play_lines]
current_year_plays = {}
for play_line in current_play_lines:
    if play_line == "":
        continue
    play_game, play_count = play_line.split(';')
    play_count = int(play_count)
    current_year_plays[play_game] = play_count
    THIS_YEAR_PLAYS += play_count

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

    game_goals = {}
    TOTAL_PLAYS_GOAL = 0
    for game_name, game_plays in game_plays_total.items():
        # Take the highest of last year's plays, or average plays per year
        avg_plays = math.ceil(game_plays / game_year_counter[game_name])
        last_year_plays = prev_year_plays.get(game_name, 0)
        goal_plays = max(avg_plays, last_year_plays + 1)
        game_goals[game_name] = goal_plays
        TOTAL_PLAYS_GOAL += goal_plays

    # Figure out today's date progress as a percentage of the year
    from datetime import datetime
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    end_of_year = datetime(now.year + 1, 1, 1)
    year_progress = (now - start_of_year).total_seconds() / \
        (end_of_year - start_of_year).total_seconds()

    # Now, given our current year progress, determine how many plays we should have
    # And then print out the top 10 games by how far off that goal we are
    game_progress = []
    TOTAL_PLAYS = 0
    completed_games = []
    new_games = []
    for game_name, _ in current_year_plays.items():
        if game_name not in game_goals:
            # Game not played last year, so just make it a goal of 1
            game_goals[game_name] = 1
            TOTAL_PLAYS_GOAL += 1
            new_games.append(game_name)
    for game_name, goal_plays in game_goals.items():
        current_plays = current_year_plays.get(game_name, 0)
        if current_plays >= goal_plays:
            TOTAL_PLAYS += goal_plays
            if game_name in new_games:
                game_name += " (New Game)"
            completed_games.append(game_name)
            continue
        expected_plays = goal_plays * year_progress
        TOTAL_PLAYS += current_plays
        progress_diff = current_plays - expected_plays
        game_progress.append((game_name, current_plays, expected_plays, progress_diff))
    game_progress = sorted(game_progress, key=lambda x:x[3])
    double_print("\nTop 10 Games Behind Expected Play Count (based on " + \
        f"{year_progress*100:.2f}% of year):", out_file_h)
    for game_info in game_progress[:10]:
        info_n, info_c, info_e, _ = game_info
        info_g = game_goals.get(info_n, 0)
        info_diff = info_e - info_c
        if info_diff > 0:
            PT_STR = f"- {info_n}: {info_c} plays out of {info_g} ({info_diff:.2f} behind)"
        else:
            PT_STR = f"- {info_n}: {info_c} plays out of {info_g} ({info_diff:.2f} ahead)"
        double_print(PT_STR, out_file_h)

    # Figure out what percentage of the total plays goal we've achieved
    # And then print out how far off pace we are
    total_plays_percentage = TOTAL_PLAYS * 100 / TOTAL_PLAYS_GOAL
    expected_pace = year_progress * TOTAL_PLAYS_GOAL
    pace_diff = TOTAL_PLAYS - expected_pace
    total_plays_string = f"\nTotal Plays so far: {TOTAL_PLAYS} out of " + \
        f"{TOTAL_PLAYS_GOAL} ({total_plays_percentage:.2f} percent)"
    double_print(total_plays_string, out_file_h)
    pace_string = f"At {year_progress*100:.2f}% of the year, you should have " + \
        f"played {expected_pace:.2f} games. You are {'ahead' if pace_diff >= 0 else 'behind'} " + \
        f"pace by {abs(pace_diff):.2f} plays."
    double_print(pace_string, out_file_h)
    total_play_str = f"In total, you have played {THIS_YEAR_PLAYS} games this year, " + \
        f"compared to {PREV_YEAR_PLAY_TOTAL} last year."
    double_print(total_play_str, out_file_h)
    double_print(f"Completed Games List: ({len(completed_games)})", out_file_h)
    for comp_game in sorted(completed_games):
        double_print(f"- {comp_game}", out_file_h)

    out_file_h.close()
