#!/usr/bin/python3

"""
Collection manager/purchase suggester for the Gundam GCG
"""

import os

from card_games.General.Libraries.deck import Deck
from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Gundam Card Game"

CURRENT_DECK_ERA = "GD03"

valid_rarities = ['C', 'U', 'R', 'LR']
valid_types = ['Unit', 'Command', 'Base', 'Pilot', ]
valid_colors = ['Red', 'Blue', 'Green', 'White', 'Purple']

FILE_PREFIX = os.path.join("card_games", "G", "Gundam_Card_Game")
DECK_PREFIX = os.path.join(FILE_PREFIX, 'Decks', CURRENT_DECK_ERA)
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = os.path.join("G", "Gundam_Card_Game")

file_h = open(os.path.join(FILE_PREFIX, 'Data', 'Gundam GCG Card Data.txt'), 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
card_mapping = {}
card_inv_dict = {}
most_needed_cards = {}
for line in lines:
    line = line.split('#')[0].strip()
    try:
        card_name, card_number, card_rarity, card_block, card_lvl, card_cost, card_color, \
            card_type, card_traits, card_sets, card_own = line.split(';')
    except ValueError:
        print("Invalid line:")
        print(line)
        continue

    card_mapping[card_number] = card_name
    if card_rarity not in valid_rarities:
        print(f"Invalid card rarity {card_rarity} for {card_name}")
    card_block = int(card_block)
    card_lvl = int(card_lvl)
    card_cost = int(card_cost)
    if card_color not in valid_colors:
        print(f"Invalid card color {card_color} for {card_name}")
    if card_type not in valid_types:
        print(f"Invalid card type {card_type} for {card_name}")
    card_traits = card_traits.split('/')
    card_sets = card_sets.split('/')
    card_own = int(card_own)
    card_inv_dict[card_number] = card_own
    CARD_MAX = 4
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    if card_own < CARD_MAX:
        most_needed_cards[card_number] = CARD_MAX - card_own
    item_list.append((card_name, card_number, card_rarity, card_block, card_lvl, card_cost, \
        card_color, card_type, card_traits, card_sets, card_own, CARD_MAX))

#Filter by set
chosen_set, filtered_list = sort_and_filter(item_list, 9)

# Filter by card_color
chosen_color, filtered_list = sort_and_filter(filtered_list, 6)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 7)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

# Begin processing decks
decks = []
for deck_colors in os.listdir(DECK_PREFIX):
    this_deck_colors = deck_colors.split('-')
    for deck_file in os.listdir(os.path.join(DECK_PREFIX, deck_colors)):
        if not deck_file.endswith('.txt'):
            print("Skipping non-txt file in decks folder:", deck_file)
            continue
        deck_path = os.path.join(DECK_PREFIX, deck_colors, deck_file)
        with open(deck_path, 'r', encoding="UTF-8") as deck_h:
            deck_lines = deck_h.readlines()
        deck_lines = [line.strip() for line in deck_lines if line.strip() != '' and
                not line.startswith('//') and not line.startswith('#')]
        deck_dict = {}
        for deck_line in deck_lines:
            try:
                deck_card_qty = int(deck_line.split(' ')[0])
                DECK_CARD_NUMBER = deck_line.split(' ')[1]
                DECK_CARD_NAME = ' '.join(deck_line.split(' ')[2:]).strip()
                DECK_CARD_NAME = DECK_CARD_NAME.split('|', maxsplit=1)[0].strip()
            except ValueError:
                print(f"Invalid deck line in {deck_path}: {deck_line}")
                continue
            DECK_CARD_NAME = DECK_CARD_NAME.replace(' III', ' Ⅲ').strip()
            DECK_CARD_NAME = DECK_CARD_NAME.replace(' II', ' Ⅱ').strip()
            if DECK_CARD_NUMBER not in card_mapping:
                print(f"Unknown card {DECK_CARD_NAME} in deck {deck_path}")
            if DECK_CARD_NAME != card_mapping[DECK_CARD_NUMBER]:
                print(card_mapping[DECK_CARD_NUMBER])
                print(f"Card name/number mismatch for {DECK_CARD_NAME} in deck {deck_path}")
            if DECK_CARD_NUMBER not in deck_dict:
                deck_dict[DECK_CARD_NUMBER] = 0
            deck_dict[DECK_CARD_NUMBER] += deck_card_qty
        this_deck = Deck(deck_file[:-4], deck_dict, {'colors': this_deck_colors})
        this_deck.update_missing_cards(card_inv_dict)
        decks.append(this_deck)

for deck in decks:
    for card_name, missing_qty in deck.deck_missing_cards.items():
        if card_name not in most_needed_cards:
            most_needed_cards[card_name] = 0
        most_needed_cards[card_name] += missing_qty

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/Gundam GCG Out.txt", 'w', encoding="UTF-8")

    double_print("Gundam Card Game Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    SUGG_STRING = f"Buy {picked_item[0]} ({chosen_color + ' ' + chosen_type}) from " + \
        f"{picked_item[1]} (have {picked_item[10]} out of {picked_item[11]})"
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
