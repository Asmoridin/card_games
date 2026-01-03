#!/usr/bin/python3

"""
Collection manager/purchase suggester for the Pokemon TCG.
"""

import os
import re

from card_games.General.Libraries.deck import Deck
from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Pokemon TCG"

CURRENT_DECK_ERA = "2025 - SVI-PFL"

valid_rarities = ['Common', 'Uncommon', 'Rare', 'Illustration Rare', 'Ultra Rare', 'Double Rare',
    'Special Illustration Rare', 'Black White Rare', 'Promo', 'Rare Holo', 'Rare Ultra',
    'Rare Rainbow', 'TGU', 'Rare Secret', 'Mega Hyper Rare', 'Hyper Rare', 'Shiny Rare',
    'ACE SPEC Rare', 'TGH', 'Rare Shiny']
valid_types = ['Pokemon', 'Trainer', 'Energy']
valid_colors = ['Fire', 'Water', 'Grass', 'Psychic', 'Darkness', 'Metal', 'Lightning', 'Fairy',
    'Colorless', 'Fighting', 'Dragon']
trainer_subtypes = ['Supporter', 'Item', 'Stadium', 'Pokemon Tool']

color_mapping = {
    'Darkness Energy': 'Darkness',
    'Fighting Energy': 'Fighting',
    'Fire Energy': 'Fire',
    'Grass Energy': 'Grass',
    'Lightning Energy': 'Lightning',
    'Metal Energy': 'Metal',
    'Psychic Energy': 'Psychic',
    'Water Energy': 'Water',
}

FILE_PREFIX = os.path.join("card_games", "P", "Pokemon")
DECK_PREFIX = os.path.join(FILE_PREFIX, 'Decks', CURRENT_DECK_ERA)
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = os.path.join("P", "Pokemon")

def process_sets(sets_string, in_set_dict, this_card_name):
    """
    Take a string of sets, and valid and process them into a list of tuples.
    
    :param sets_string: Sets string from the data file.
    :return: List of tuples of (set_ids, rarities).
    """
    sets = sets_string.split('/')
    set_info = []
    set_rarities = set()
    for set_entry in sets:
        set_entry = set_entry.strip()
        set_match = re.match(r'^(.*?) (\d+) \((.*?)\)$', set_entry)
        if set_match:
            this_set_name = set_match.group(1).strip()
            if this_set_name not in in_set_dict.keys():
                print(f"Unknown set name {this_set_name} for card {this_card_name}")
            this_set_name = in_set_dict.get(this_set_name, this_set_name)
            set_num = set_match.group(2).strip()
            set_rarity = set_match.group(3).strip()
            if set_rarity not in valid_rarities:
                print(f"Invalid rarity {set_rarity} for card {this_card_name} in set {set_entry}")
            set_info.append(f"{this_set_name} {set_num}")
            set_rarities.add(set_rarity)
        else:
            print(f"Invalid set entry format: {set_entry} for card {this_card_name}")
    return (sorted(set_info), list(set_rarities))

set_dict = {}
SET_FILE = os.path.join(FILE_PREFIX, 'Data', 'Pokemon Sets.txt')
with open(SET_FILE, 'r', encoding="UTF-8") as set_file_h:
    set_lines = set_file_h.readlines()

for set_line in set_lines:
    set_line = set_line.split('#')[0]
    set_line = set_line.strip()
    if set_line == '' or set_line.startswith('#'):
        continue
    if ';' in set_line:
        try:
            set_id, set_name = set_line.split(';')
        except ValueError:
            print("Invalid set line:")
            print(set_line)
            continue
    else:
        set_id = set_line
        set_name = set_line
    set_dict[set_id.strip()] = set_name.strip()

file_h = open(os.path.join(FILE_PREFIX, 'Data', 'Pokemon Card Data.txt'), 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
card_mapping = {}
card_inv_dict = {}
most_needed_cards = {}
card_num_mapping = {} # Maps all card numbers to their singular 'canonical' number
for line in lines:
    line = line.split('#')[0].strip()
    if line == '':
        continue
    try:
        card_name, card_type, card_color, card_hp, card_ability, card_moves, card_sets, \
            card_marks, card_max, card_own = line.split(';')
    except ValueError:
        print("Invalid line:")
        print(line)
        continue

    if card_type not in valid_types:
        print(f"Invalid card type {card_type} for {card_name}")

    if card_type == "Pokemon" and card_color not in valid_colors:
        print(f"Invalid card color {card_color} for {card_name}")
    if card_type == "Trainer" and card_color not in trainer_subtypes:
        print(f"Invalid trainer subtype {card_color} for {card_name}")

    if card_hp != '':
        card_hp = int(card_hp)
    else:
        card_hp = None
    card_moves = card_moves.split('|')
    card_sets, card_rarities = process_sets(card_sets, set_dict, card_name)
    card_id = card_sets[0]
    for card_set in card_sets:
        card_num_mapping[card_set] = card_id
        card_mapping[card_id] = card_name
    card_marks = card_marks.split('/')

    card_max = int(card_max)
    card_own = int(card_own)

    card_inv_dict[card_id] = card_own
    TOTAL_OWN += card_own
    TOTAL_MAX += card_max
    if card_own < card_max:
        most_needed_cards[card_id] = card_max - card_own
    item_list.append((card_id, card_name, card_type, card_color, card_hp, card_ability, \
        card_moves, card_sets, card_rarities, card_marks, card_own, card_max))

#Filter by set
chosen_set, filtered_list = sort_and_filter(item_list, 7)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 2)

# Filter by card_color
chosen_color, filtered_list = sort_and_filter(filtered_list, 3)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 1)
picked_item = filtered_list[0]

# Begin processing decks
decks = []
for deck_file in os.listdir(DECK_PREFIX):
    if not deck_file.endswith('.txt'):
        print("Skipping non-txt file in decks folder:", deck_file)
        continue
    deck_path = os.path.join(DECK_PREFIX, deck_file)
    with open(deck_path, 'r', encoding="UTF-8") as deck_h:
        deck_lines = deck_h.readlines()
    deck_lines = [line.strip() for line in deck_lines if line.strip() != '' and
            not line.startswith('//') and not line.startswith('#')]
    deck_dict = {}
    this_deck_colors = set()
    PROCESS_ENERGY = False
    for deck_line in deck_lines:
        if deck_line.startswith('Pokémon: ') or deck_line.startswith('Trainer: '):
            continue
        if deck_line.startswith('Energy: '):
            PROCESS_ENERGY = True
            continue
        match = re.match(r'^(\d+) (.*) (...) (\d+)$', deck_line)
        if match:
            deck_card_qty = int(match.group(1))
            DECK_CARD_NAME = match.group(2)
            deck_card_set = match.group(3)
            deck_card_set_number = match.group(4)
        else:
            print(f"Invalid deck line in {deck_path}: {deck_line}")
            continue
        deck_card_set = set_dict.get(deck_card_set, deck_card_set)
        deck_card_id = deck_card_set + ' ' + deck_card_set_number
        if deck_card_id not in card_num_mapping:
            print(f"Unknown card {DECK_CARD_NAME} ({deck_card_id}) in deck {deck_path}")
        deck_card_id = card_num_mapping.get(deck_card_id, deck_card_id)
        if PROCESS_ENERGY:
            COLORLESS_ENERGY = ['Enriching Energy', 'Jet Energy', 'Legacy Energy',
                'Luminous Energy', 'Mist Energy']
            if DECK_CARD_NAME in color_mapping:
                mapped_color = color_mapping.get(DECK_CARD_NAME, DECK_CARD_NAME)
                this_deck_colors.add(mapped_color)
            elif DECK_CARD_NAME in COLORLESS_ENERGY:
                pass
            else:
                print(f"Unknown energy card {DECK_CARD_NAME} in deck {deck_path}")
        if deck_card_id not in deck_dict:
            deck_dict[deck_card_id] = 0
        deck_dict[deck_card_id] += deck_card_qty
    if this_deck_colors == set():
        this_deck_colors.add('Colorless')
    this_deck = Deck(deck_file[:-4], deck_dict, {'colors': this_deck_colors})
    this_deck.update_missing_cards(card_inv_dict)
    decks.append(this_deck)

for deck in decks:
    for card_name, missing_qty in deck.deck_missing_cards.items():
        if card_name not in most_needed_cards:
            most_needed_cards[card_name] = 0
        most_needed_cards[card_name] += missing_qty

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/Pokemon TCG Out.txt", 'w', encoding="UTF-8")

    double_print("Pokemon TCG Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    SUGG_STRING = f"Buy {picked_item[1]} ({chosen_type + ' ' + chosen_color}) from " + \
        f"{chosen_set} (have {picked_item[10]} out of {picked_item[11]})"
    double_print(SUGG_STRING, out_file_h)

    double_print("\nMost needed cards:", out_file_h)
    sorted_most_needed = sorted(most_needed_cards.items(), key=lambda x: (-x[1], x[0]))
    for card_num, needed_qty in sorted_most_needed[:10]:
        NEED_STR = f" - {card_mapping.get(card_num, card_num)} ({card_num}): {needed_qty} cards"
        double_print(NEED_STR, out_file_h)

    sorted_decks = sorted(decks, key=lambda x: x.get_num_missing_cards())
    double_print("\nDecks closest to completion:", out_file_h)
    used_colors = set()
    for deck in sorted_decks:
        if deck.get_num_missing_cards() == 0:
            double_print(f" - Completed deck: {deck.deck_name}", out_file_h)
            continue
        PROCESS_DECK = True
        for color in deck.deck_tags['colors']:
            if color in used_colors:
                PROCESS_DECK = False
        if not PROCESS_DECK:
            continue
        used_colors.update(deck.deck_tags['colors'])
        PRINT_DECK_NAME = f"{deck.deck_name} ({'/'.join(sorted(deck.deck_tags['colors']))})"
        double_print(f" - {PRINT_DECK_NAME}: {deck.get_num_missing_cards()} cards", out_file_h)
        for card_num, missing_qty in sorted(deck.deck_missing_cards.items()):
            CARD_STR = f"    - {card_mapping.get(card_num, card_num)} ({card_num}): {missing_qty}"
            double_print(CARD_STR, out_file_h)

    out_file_h.close()
