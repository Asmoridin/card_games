#!/usr/bin/python3

"""
Collection manager/purchase suggester for Riftbound
"""

import os
import re

from card_games.General.Libraries.deck import Deck
from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Riftbound"
DECK_ERA = "02 - Spiritforged"

def parse_sets(set_string, this_card_name=""):
    """
    Generates a list of card sets, and rarities, for cards
    
    :param card_sets: A / seperated list of printings
    """
    ret_sets = []
    ret_rarities = set()
    for set_part in set_string.split('/'):
        match_obj = re.search(r"(.*) \((.*)\)", set_part)
        if match_obj:
            this_set, this_set_rarity = match_obj.groups()
            ret_sets.append(this_set)
            ret_rarities.add(this_set_rarity)
        else:
            print("[" + this_card_name + "] Issue with: " + set_part)
    return (ret_sets, list(ret_rarities))

valid_types = ['Unit', 'Spell', 'Battlefield', 'Legend', 'Champion Unit', 'Gear', 'Rune',
    'Signature Spell', 'Signature Unit', 'Signature Gear', ]
valid_colors = ['Chaos', 'Body', 'Mind', 'Order', 'Fury', 'Colorless', 'Calm']

FILE_PREFIX = "card_games/R/Riftbound"
DECK_PREFIX = FILE_PREFIX + "/Decks"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "R/Riftbound"

file_h = open(FILE_PREFIX + '/Data/Riftbound Data.txt', 'r', encoding="UTF-8")

with open(FILE_PREFIX + '/Data/Used Tags.txt', 'r', encoding="UTF-8") as in_tags:
    used_tags = in_tags.readlines()
used_tags = [line.strip() for line in used_tags if line.strip() != '']

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
legends = set()
tags = {}
card_names = set()
card_inv_dict = {}
most_needed_cards = {}
for line in lines:
    line = line.split('#')[0].strip()
    line_vals = line.split(';')
    temp_max = None
    if len(line_vals) == 9:
        card_name, card_type, card_color, card_traits, card_cost, card_power, card_might, \
            card_sets, card_own = line_vals
    elif len(line_vals) == 10:
        card_name, card_type, card_color, card_traits, card_cost, card_power, card_might, \
            card_sets, card_own, temp_max = line_vals
    else:
        print("Invalid line:")
        print(line)
        continue

    if card_type not in valid_types:
        print(f"Invalid card type {card_type} for {card_name}")
    card_colors = card_color.split('/')
    for card_color in card_colors:
        if card_color not in valid_colors:
            print(f"Invalid card color {card_color} for {card_name}")
    card_traits = card_traits.split('/')
    for trait in card_traits:
        if trait != '':
            if trait not in tags:
                tags[trait] = 0
            tags[trait] += 1
    card_cost = int(card_cost) if card_cost.isdigit() else card_cost
    card_power = int(card_power) if card_power.isdigit() else card_power

    card_sets, card_rarities = parse_sets(card_sets, card_name)

    card_own = int(card_own)
    CARD_MAX = 3
    if card_type == 'Legend':
        card_name = card_traits[0] + ", " + card_name
        CARD_MAX = 1
        legends.add(card_name)
    elif card_type == 'Battlefield':
        CARD_MAX = 2
    elif card_type == 'Rune':
        CARD_MAX = 12
    elif temp_max is not None and temp_max.isdigit():
        CARD_MAX = int(temp_max)

    if card_name in card_names:
        print(f"Duplicate card name found: {card_name}")
    else:
        card_names.add(card_name)

    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    if card_own < CARD_MAX:
        most_needed_cards[card_name] = CARD_MAX - card_own
    card_inv_dict[card_name] = card_own
    item_list.append((card_name, card_type, card_colors, card_traits, card_cost, card_power, \
            card_might, card_sets, card_rarities, card_own, CARD_MAX))

# Being processing decks
decks = []
PROCESS_DECK_DIR = os.path.join(DECK_PREFIX, DECK_ERA)
for color_dir in os.listdir(PROCESS_DECK_DIR):
    color_path = os.path.join(PROCESS_DECK_DIR, color_dir)
    deck_colors = color_dir.split('-')
    if not os.path.isdir(color_path):
        continue
    for deck_file in os.listdir(color_path):
        if not deck_file.endswith('.txt'):
            continue
        deck_path = os.path.join(color_path, deck_file)
        with open(deck_path, 'r', encoding="UTF-8") as deck_h:
            deck_lines = deck_h.readlines()
        deck_lines = [line.strip() for line in deck_lines if line.strip() != '' and
            not line.startswith('#')]
        deck_dict = {}
        for deck_line in deck_lines:
            if deck_line in ['Legend:', 'Runes:', 'Battlefields:', 'Sideboard:', 'Champion:',
                    'MainDeck:']:
                continue
            try:
                deck_card_qty = int(deck_line.split(' ')[0])
                DECK_CARD_NAME = ' '.join(deck_line.split(' ')[1:]).strip()
            except ValueError:
                print(f"Invalid deck line in {deck_path}: {deck_line}")
                continue
            if DECK_CARD_NAME not in card_names:
                print(f"Unknown card {DECK_CARD_NAME} in deck {deck_path}")
            if DECK_CARD_NAME not in deck_dict:
                deck_dict[DECK_CARD_NAME] = 0
            deck_dict[DECK_CARD_NAME] += deck_card_qty
        this_deck = Deck(deck_file[:-4], deck_dict, {'colors': deck_colors})
        this_deck.update_missing_cards(card_inv_dict)
        decks.append(this_deck)

for deck in decks:
    for card_name, missing_qty in deck.deck_missing_cards.items():
        if card_name not in most_needed_cards:
            most_needed_cards[card_name] = 0
        most_needed_cards[card_name] += missing_qty

#Filter by set
chosen_set, filtered_list = sort_and_filter(item_list, 7)

# Filter by card_color
chosen_color, filtered_list = sort_and_filter(filtered_list, 2)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 1)

# Filter by rarity
chosen_rarity, filtered_list = sort_and_filter(filtered_list, 8)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/Riftbound Out.txt", 'w', encoding="UTF-8")

    double_print("Riftbound Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    double_print(f"{len(legends)} different legends in the game\n", out_file_h)

    SUGG_STRING = f"Buy {picked_item[0]} ({chosen_color + ' ' + chosen_type}) from " + \
        f"{picked_item[7]} (have {picked_item[-2]} out of {picked_item[-1]})"
    double_print(SUGG_STRING, out_file_h)

    for trait in used_tags:
        if trait in tags:
            del tags[trait]
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    double_print("\nMost common unused tags:", out_file_h)
    for tag, count in sorted_tags[:10]:
        double_print(f" - {tag}: {count} cards", out_file_h)

    double_print("\nMost needed cards:", out_file_h)
    sorted_most_needed = sorted(most_needed_cards.items(), key=lambda x: (-x[1], x[0]))
    for card_name, needed_qty in sorted_most_needed[:10]:
        double_print(f" - {card_name}: {needed_qty} cards", out_file_h)

    sorted_decks = sorted(decks, key=lambda x: x.get_num_missing_cards())
    double_print("\nDecks closest to completion:", out_file_h)
    used_colors = set()
    for deck in sorted_decks:
        if len(used_colors) >= 6:
            break
        PROCESS_DECK = True
        for color in deck.deck_tags['colors']:
            if color in used_colors:
                PROCESS_DECK = False
        if not PROCESS_DECK:
            continue
        for color in deck.deck_tags['colors']:
            used_colors.add(color)
        double_print(f" - {deck.deck_name}: {deck.get_num_missing_cards()} cards", out_file_h)
        for card_name, missing_qty in sorted(deck.deck_missing_cards.items()):
            double_print(f"    - {card_name}: {missing_qty}", out_file_h)

    out_file_h.close()
