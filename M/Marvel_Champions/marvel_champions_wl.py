#!/usr/bin/python3

"""
List wins and losses for Marvel Champions, and give recommendations for what to play next
"""

import os
import random
from card_games.General.Libraries.output_utils import double_print
from card_games.M.Marvel_Champions.Libraries import marvel_champions_encounters as ChampEncounters
from card_games.M.Marvel_Champions.Libraries import marvel_champions_heroes as ChampHeroes

FILE_PREFIX = "card_games/M/Marvel_Champions"
if os.getcwd().endswith('card_games'):
    FILE_PREIFIX = "M/Marvel_Champions"

file_h = open(FILE_PREFIX + '/Data/ChampionsPlayedHeroes.txt', 'r', encoding="UTF-8")
enc_file_h = open(FILE_PREFIX + '/Data/ChampionsPlayedEncounters.txt', 'r', encoding="UTF-8")

TOTAL_HERO_CHOICES = len(ChampHeroes.hero_combinations)

def get_hero_wl(in_hero, in_aspect, in_play_map):
    """
    For a given hero and aspect, return the total wins and losses
    """
    ret_hero_wins = 0
    ret_hero_losses = 0
    if (in_hero, in_aspect) in in_play_map:
        ret_hero_wins = in_play_map[(in_hero, in_aspect)][1]
        ret_hero_losses = in_play_map[(in_hero, in_aspect)][0] - ret_hero_wins
    return((ret_hero_wins, ret_hero_losses))

def get_encounter_wl(encounter, mod_encounters, encounter_map):
    """
    For a given encounter, determine the total wins and losses
    """
    ret_wins = 0
    ret_losses = 0
    mod_encounters = tuple(sorted(mod_encounters))
    if (encounter, mod_encounters) in encounter_map:
        ret_wins = encounter_map[(encounter, mod_encounters)][1]
        ret_losses = encounter_map[(encounter, mod_encounters)][0] - ret_wins
    return((ret_wins, ret_losses))

def determine_combinations():
    """
    Return the number of different hero combinations I can play.
    """
    combinations = set()
    h_1 = ChampHeroes.hero_combinations
    h_2 = ChampHeroes.hero_combinations
    for combo_1 in h_1:
        for combo_2 in h_2:
            if combo_1[0] != combo_2[0] and combo_1[1] != combo_2[1]:
                this_combo = sorted([combo_1, combo_2])
                combinations.add(tuple(this_combo))
    return len(combinations)

def get_hero_stats(play_map):
    """
    Given a map of game plays, return a tuple with the following information:
    - most played hero name
    - number of games with most played hero
    - least played hero name
    - number of games with least played hero
    """
    sum_map = {} # Need to sum up the plays by each hero
    for this_hero in ChampHeroes.heroes:
        sum_map[this_hero.name] = 0
    for (this_hero, this_aspect) in play_map:
        sum_map[this_hero] += play_map[(this_hero, this_aspect)][0]
    hero_list = []
    for this_hero, hero_plays in sum_map.items():
        hero_list.append((this_hero, hero_plays))
    hero_list = sorted(hero_list, key=lambda x:(x[1], x[0]))
    return(hero_list[-1][0], hero_list[-1][1], hero_list[0][0], hero_list[0][1])

def get_aspect_stats(play_map):
    """
    Return most played aspect, amount of times played said aspect, least played aspect,
    amount of plays for that aspect
    """
    sum_map = {}
    for set_aspect in ChampHeroes.aspects:
        sum_map[set_aspect] = 0
    for (this_hero, this_aspect_tuple) in play_map:
        for this_aspect in this_aspect_tuple:
            sum_map[this_aspect] += play_map[(this_hero, this_aspect_tuple)][0]

    aspect_tuples = []
    for this_aspect, aspect_plays in sum_map.items():
        aspect_tuples.append((this_aspect, aspect_plays))
    aspect_tuples = sorted(aspect_tuples, key=lambda x:(x[1], x[0]))
    return(aspect_tuples[-1][0], aspect_tuples[-1][1], aspect_tuples[0][0], aspect_tuples[0][1])

def get_least_played_hero(play_map):
    """
    Return the least played hero/aspect combination
    """
    least_played_hero = get_hero_stats(play_map)[2]
    combinations = ChampHeroes.hero_map[least_played_hero].gen_combos()
    aspect_combos = []
    for combination in combinations:
        if combination not in play_map:
            aspect_combos.append((combination, 0))
        else:
            aspect_combos.append((combination, play_map[combination][0]))
    aspect_combos = sorted(aspect_combos, key=lambda x:(x[1], x[0][1]))
    return(aspect_combos[0][0][0], aspect_combos[0][0][1])

def get_least_played_encounter(in_enc_played_map):
    """
    Given the list of games I've played, figure out which available villain has been
    played the least (possibly 0 times)
    """
    chosen_villain = get_villain_stats(in_enc_played_map)[2]
    if chosen_villain == 'The Hood':
        hood_encounters = sorted(random.sample(ChampEncounters.modular_encounters, 7))
        this_encounter = ('The Hood', tuple(hood_encounters))
        return this_encounter
    encounter_list = ChampEncounters.encounter_map[chosen_villain].gen_combos()
    encounter_list = sorted(encounter_list, key=lambda x:x[1])
    encounter_played = []
    for encounter_combo in encounter_list:
        if encounter_combo not in in_enc_played_map:
            return encounter_combo
        encounter_played.append((encounter_combo, in_enc_played_map[encounter_combo][0]))
    encounter_played = sorted(encounter_played, key=lambda x: x[1])
    return encounter_played[0][0]

def get_villain_stats(encounter_map):
    """
    Returns (most played villain, most played villain amount, least played villain,
    least played villain amount)
    """
    sum_map = {}
    for this_villain in ChampEncounters.encounters:
        sum_map[this_villain.name] = 0
    for played_enc in encounter_map:
        sum_map[played_enc[0]] += encounter_map[played_enc][0]
    sum_tuples = []
    for this_villain, this_villain_plays in sum_map.items():
        sum_tuples.append((this_villain, this_villain_plays))
    sum_tuples = sorted(sum_tuples, key=lambda x:(x[1], x[0]))
    return(sum_tuples[-1][0], sum_tuples[-1][1], sum_tuples[0][0], sum_tuples[0][1])

def get_modular_stats(encounter_map):
    """
    Return most played encounter set, amount it was played, least played encounter set,
    amount played
    """
    modular_sets = ChampEncounters.modular_encounters
    sum_map = {}
    for modular in modular_sets:
        sum_map[modular] = 0
    for played_enc in encounter_map:
        for modular in ChampEncounters.get_req_by_encounter(played_enc[0]):
            sum_map[modular] += encounter_map[played_enc][0]
        for modular in played_enc[1]:
            sum_map[modular] += encounter_map[played_enc][0]
    mod_tuples = []
    for modular, modular_plays in sum_map.items():
        mod_tuples.append((modular, modular_plays))
    mod_tuples = sorted(mod_tuples, key=lambda x:(x[1], x[0]))
    return(mod_tuples[-1][0], mod_tuples[-1][1], mod_tuples[0][0], mod_tuples[0][1])

# Read in and set up Hero data structures
hero_lines = file_h.readlines()
file_h.close()
hero_lines = [line.strip() for line in hero_lines]
hero_played_map = {}
PLAYED_MAX = 0
for line in hero_lines:
    hero_line = line.split(';')
    if int(hero_line[2]) > PLAYED_MAX:
        PLAYED_MAX = int(hero_line[2])
    aspects = ()
    if hero_line[1] != '':
        aspects = tuple(hero_line[1].split('/'))
    hero_played_map[(hero_line[0], aspects)] = (int(hero_line[2]), int(hero_line[3]))

# Read in and process the Encounter data structures
encounter_lines = enc_file_h.readlines()
enc_file_h.close()
encounter_lines = [line.strip() for line in encounter_lines]
enc_played_map = {}
PLAYED_MAX = 0
for line in encounter_lines:
    #TODO: encounter_line[2] is the difficulty, do we want to do anything with it?
    encounter_line = line.split(';')
    if int(encounter_line[3]) > PLAYED_MAX:
        PLAYED_MAX = int(encounter_line[3])
    encounter_sets = tuple(sorted(encounter_line[1].split('/')))
    if encounter_sets == ('',):
        encounter_sets = ()
    enc_map_key = (encounter_line[0], encounter_sets)
    enc_played_map[enc_map_key] = (int(encounter_line[3]), int(encounter_line[4]))

if __name__ == "__main__":
    OUT_FILENAME = FILE_PREFIX + "/MarvelChampionsOut.txt"
    out_file_h = open(OUT_FILENAME, 'w', encoding="UTF-8")

    double_print("Generating a game", out_file_h)
    SUMM_STR = f"There are {TOTAL_HERO_CHOICES} different Hero/Aspect combinations, and " + \
        f"{determine_combinations()} different game pairings"
    double_print(SUMM_STR, out_file_h)

    play_str = f"Currently have played {len(hero_played_map) * 100 / TOTAL_HERO_CHOICES:.1f} " + \
        "percent of Hero/Aspects"
    double_print(play_str, out_file_h)
    SUMM_STR = f"There are {len(ChampHeroes.heroes)} heroes, {len(ChampEncounters.encounters)}" + \
        f" different encounters, and {len(ChampEncounters.modular_encounters)} different " + \
        "modular encounter sets\n"
    double_print(SUMM_STR, out_file_h)

    # Choose first hero - always choose least played hero
    choice_1 = get_least_played_hero(hero_played_map)

    # Choose second hero, with lowest hero/aspect combination remaining
    choices = []
    for hero_choice in ChampHeroes.hero_combinations:
        if hero_choice[0] == choice_1[0]:
            continue
        VALID = True
        for aspect in hero_choice[1]:
            if aspect in choice_1[1]:
                VALID = False
        if not VALID:
            continue
        if (hero_choice[0], hero_choice[1]) in hero_played_map:
            choices.append((hero_choice[0], hero_choice[1],
                hero_played_map[(hero_choice[0], hero_choice[1])][0]))
        else:
            choices.append((hero_choice[0], hero_choice[1], 0))
    choices = sorted(choices, key=lambda x:(x[2], x[0], x[1]))
    choice_2 = (choices[0][0], choices[0][1])

    hero_tuple = get_hero_stats(hero_played_map)
    HERO_STR = f"Most played hero: {hero_tuple[0]} ({hero_tuple[1]} times). Least: " + \
        f"{hero_tuple[2]} ({hero_tuple[3]})"
    double_print(HERO_STR, out_file_h)
    aspect_tuple = get_aspect_stats(hero_played_map)
    ASPECT_STR = f"Most played aspect: {aspect_tuple[0]} ({aspect_tuple[1]} times). Least: " + \
        f"{aspect_tuple[2]} ({aspect_tuple[3]})"
    double_print(ASPECT_STR, out_file_h)
    scenario_tuple = get_villain_stats(enc_played_map)
    VILL_STR = f"Most played scenario: {scenario_tuple[0]} ({scenario_tuple[1]} times). Least: " + \
        f"{scenario_tuple[2]} ({scenario_tuple[3]})"
    double_print(VILL_STR, out_file_h)
    modular_tuple = get_modular_stats(enc_played_map)
    MOD_STR = f"Most played modular encounter: {modular_tuple[0]} ({modular_tuple[1]} times). " + \
        f"Least: {modular_tuple[2]} ({modular_tuple[3]})"
    double_print(MOD_STR, out_file_h)

    # Choose an encounter
    encounter_choice = get_least_played_encounter(enc_played_map)

    hero_1_wl = get_hero_wl(choice_1[0], choice_1[1], hero_played_map)
    hero_2_wl = get_hero_wl(choice_2[0], choice_2[1], hero_played_map)
    HA_STR = f"\nHeroes/Aspects chosen: {'/'.join(choice_1[1])} {choice_1[0]} ({hero_1_wl[0]}W" + \
        f"-{hero_1_wl[1]}L) and {'/'.join(choice_2[1])} {choice_2[0]} ({hero_2_wl[0]}W-" + \
        f"{hero_2_wl[1]}L)"
    double_print(HA_STR, out_file_h)
    enc_wl = get_encounter_wl(encounter_choice[0], encounter_choice[1], enc_played_map)
    ENC_STR = f"Chosen encounter is {'/'.join(encounter_choice[1])} {encounter_choice[0]} " + \
        f"({enc_wl[0]}W-{enc_wl[1]}L)"
    double_print(ENC_STR, out_file_h)

    double_print("\nTotal W-L by hero:", out_file_h)
    hero_wl = {}
    for hero_choice in ChampHeroes.hero_combinations:
        if hero_choice[0] not in hero_wl:
            hero_wl[hero_choice[0]] = [0,0]
        wins, losses = get_hero_wl(hero_choice[0], hero_choice[1], hero_played_map)
        hero_wl[hero_choice[0]][0] += wins
        hero_wl[hero_choice[0]][1] += losses
    for hero in sorted(hero_wl):
        hero_spacer = " " * (30 - len(hero))
        hero_wins = hero_wl[hero][0]
        hero_losses = hero_wl[hero][1]
        HERO_WL_STR = f"{hero}{hero_spacer}{hero_wins} - {hero_losses}"
        double_print(HERO_WL_STR, out_file_h)

    overall_wl = [0, 0]
    double_print("\nTotal W-L by villain:", out_file_h)
    villain_wl = {}
    for encounter_obj in ChampEncounters.encounters:
        villain_wl[encounter_obj.name] = [0, 0]
    for villain_choice in enc_played_map:
        if villain_choice[0] not in villain_wl:
            villain_wl[villain_choice[0]] = [0,0]
        wins, losses = get_encounter_wl(villain_choice[0], villain_choice[1], enc_played_map)
        villain_wl[villain_choice[0]][0] += wins
        overall_wl[0] += wins
        villain_wl[villain_choice[0]][1] += losses
        overall_wl[1] += losses

    for villain in sorted(villain_wl):
        villain_spacer = " " * (30-len(villain))
        villain_wins = villain_wl[villain][0]
        villains_losses = villain_wl[villain][1]
        VILLAIN_WL_STR = f"{villain}{villain_spacer}{villain_wins} - {villains_losses}"
        double_print(VILLAIN_WL_STR, out_file_h)

    double_print("\nTotal W-L by aspect:", out_file_h)
    aspect_wl = {}
    for hero_choice in ChampHeroes.hero_combinations:
        for aspect in hero_choice[1]:
            if aspect not in aspect_wl:
                aspect_wl[aspect] = [0,0]
            wins, losses = get_hero_wl(hero_choice[0], hero_choice[1], hero_played_map)
            aspect_wl[aspect][0] += wins
            aspect_wl[aspect][1] += losses
    double_print(str(aspect_wl), out_file_h)

    overall_win_pct = overall_wl[0]/(overall_wl[0] + overall_wl[1])
    wl_str = f"\nWin Loss Records, Overall: {overall_wl[0]} - {overall_wl[1]}, " + \
        f"{overall_win_pct:.3f}"
    double_print(wl_str, out_file_h)
