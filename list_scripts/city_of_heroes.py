#!/usr/bin/python3

"""
Collection tracker and purchase suggestion tool for the City of Heroes card game
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "City of Heroes"

def validate_type(in_type):
    """
    Standardize the card types
    """
    if in_type in ['Power'] or 'Sig Power' in in_type or in_type.startswith('Power •'):
        return "Power"
    if in_type in ['Mission'] or in_type.startswith('Mission'):
        return "Mission"
    if in_type in ['Enhancement', 'Edge']:
        return in_type
    if in_type.startswith('Sidekick'):
        return 'Sidekick'
    if in_type.startswith('Hero'):
        return 'Hero'
    print("Invalid type: " + in_type)
    return None

def validate_powers(in_power):
    """
    Standard the card powers
    """
    valid_powers = ['War Mace', 'Trick Arrow', 'Super Strength', 'Super Reflexes',
        'Storm Summoning', 'Stone Melee', 'Stone Armor', 'Spines', 'Sonic Resonance',
        'Sonic Attack', 'Regeneration', 'Radiation Emission', 'Radiation Blast', 'Psychic Blast',
        'Mind Control', 'Martial Arts', 'Kinetics', 'Katana', 'Invulnerability',
        'Illusion Control', 'Ice Melee', 'Ice Manipulation', 'Ice Control', 'Ice Blast',
        'Ice Armor', 'Gravity Control', 'Force Field', 'Fire Manipulation', 'Fire Control',
        'Fire Blast', 'Fiery Melee', 'Fiery Aura', 'Energy Melee', 'Energy Manipulation',
        'Energy Blast', 'Empathy', 'Electrical Manipulation', 'Electrical Blast',
        'Earth Control', 'Devices', 'Dark Miasma', 'Dark Melee', 'Dark Blast', 'Dark Armor',
        'Common Pool', 'Claws', 'Broad Sword', 'Battle Axe', 'Assault Rifle', 'Archery'
    ]
    if in_power in valid_powers:
        return in_power
    if in_power.replace(' 1', '') in valid_powers:
        return in_power.replace(' 1', '')
    if in_power.replace(' 2', '') in valid_powers:
        return in_power.replace(' 2', '')
    if in_power.replace(' 3', '') in valid_powers:
        return in_power.replace(' 3', '')
    if in_power.replace(' 4', '') in valid_powers:
        return in_power.replace(' 4', '')
    if in_power.replace(' 6', '') in valid_powers:
        return in_power.replace(' 6', '')
    print("Invalid Power: " + in_power)
    return None

if os.getcwd().endswith('card_games'):
    file_h = open('DB/CityOfHeroesData.txt', 'r', encoding="UTF-8")
else:
    file_h = open('card_games/DB/CityOfHeroesData.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
NUM_HEROES = 0
for line in lines:
    line = line.split('//')[0]
    card_name, card_type, card_powers, card_rarity, card_set, card_own = line.split(';')
    card_type = validate_type(card_type)
    if card_type == "Power":
        card_powers = validate_powers(card_powers)
    card_own = int(card_own)
    if card_type == 'Hero':
        CARD_MAX = 1
        NUM_HEROES += 1
    else:
        CARD_MAX = 3
    TOTAL_MAX += CARD_MAX
    TOTAL_OWN += card_own
    item_list.append((card_name, card_type, card_powers, card_rarity, card_set, card_own, CARD_MAX))

# Filter by set
chosen_set, filtered_list = sort_and_filter(item_list, 4)

# Filter by card type
chosen_type, filtered_list = sort_and_filter(filtered_list, 1)
#print(chosen_type)

CHOSEN_POWER = ''
if chosen_type == 'Power':
    CHOSEN_POWER, filtered_list = sort_and_filter(filtered_list, 2)
#print(CHOSEN_POWER)

# Choose card
pick_name, filtered_list = sort_and_filter(filtered_list, 0)
#print(pick_name)
picked_item = filtered_list[0]

if __name__=="__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("output/CityOfHeroesOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/output/CityOfHeroesOut.txt", 'w', encoding="UTF-8")

    double_print("City of Heroes CCG Inventory Tracker Tool\n", out_file_h)

    double_print(f"There are {NUM_HEROES} heroes in the game\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)
    buy_str = f"Buy {picked_item[0]} ({picked_item[1]}) from {picked_item[4]} (have " + \
        f"{picked_item[5]} out of {picked_item[6]})"
    double_print(buy_str, out_file_h)

    out_file_h.close()
