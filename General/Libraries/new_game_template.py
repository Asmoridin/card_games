#!/usr/bin/python3

"""
Collection manager/purchase suggester for a XXXXX. Reads in card data and deck lists, tracks
collection ownership, and suggests cards to acquire based on missing cards in decks and overall
collection needs. Also tracks win-loss records by various categories for strategic insights.
"""

import os

from card_games.General.Libraries.deck import Deck
from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "XXXXX"

# Define valid values for card attributes
valid_types = ['Character', 'Event', 'Site', 'Action Point']
valid_colors = ['Green', 'Yellow', 'Blue', 'Purple', 'Red']
valid_rarities = ['C', 'U', 'R', 'SR', 'SP', ]
valid_triggers = ['', 'Active', 'Draw', 'Color', 'Raid', 'Special', 'Final', 'Get']

# Set up directory paths
FILE_PREFIX = os.path.join("card_games", "X", "XXXXX")
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = os.path.join("X", "XXXXX")
DECK_PREFIX = os.path.join(FILE_PREFIX, "Decks")
DATA_PREFIX = os.path.join(FILE_PREFIX, "Data")

# Pull in card data
with open(os.path.join(DATA_PREFIX, "XXXXX Data.txt"), 'r', encoding="UTF-8") as file_h:
    lines = file_h.readlines()
lines = [line.strip() for line in lines]

# Pull in additional data files, and set up data structures
with open(os.path.join(DATA_PREFIX, "XXXXX Sets.txt"), 'r', encoding="UTF-8") as in_sets:
    game_sets = in_sets.readlines()
game_sets = [line.strip() for line in game_sets if line.strip() != '']

with open(os.path.join(DATA_PREFIX, "XXXXX WL Data.txt"), 'r', encoding="UTF-8") as in_wl:
    game_wl = in_wl.readlines()
game_wl = [line.strip() for line in game_wl if line.strip() != '']

# Read in the card data, validating and organizing as we go. Track total ownership and max
# for collection completion percentage.
TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
card_inv_dict = {}
most_needed_cards = {}
for line in lines:
    if line == '' or line.startswith('#'):
        continue
    line = line.split('#')[0].strip()

    CARD_MAX = 4
    line_vals = line.split(';')

    if len(line_vals) == 6:
        card_name, card_rarity, card_type, card_color, card_sets, card_own = line_vals
    else:
        print("Invalid line:")
        print(line)
        continue

    # Validate card data
    if card_rarity not in valid_rarities:
        print(f"Invalid card rarity {card_rarity} for {card_name}")
    if card_type not in valid_types:
        print(f"Invalid card type {card_type} for {card_name}")

    card_sets = card_sets.split('/')
    card_own = int(card_own)

    # With card data now validated, populate our structures
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    if card_own < CARD_MAX:
        most_needed_cards[card_name] = CARD_MAX - card_own
    card_inv_dict[card_name] = card_own
    item_list.append((card_name, card_rarity, card_type, card_color, card_sets, \
        card_own, CARD_MAX))

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
    for deck_line in deck_lines:
        try:
            deck_card_qty = int(deck_line.split(' ')[0])
            deck_card_name = ' '.join(deck_line.split(' ')[1:]).strip()
        except ValueError:
            print(f"Invalid deck line in {deck_path}: {deck_line}")
            continue
        if deck_card_name not in card_inv_dict:
            print(f"Unknown card {deck_card_name} in deck {deck_path}")
        if deck_card_name not in deck_dict:
            deck_dict[deck_card_name] = 0
        deck_dict[deck_card_name] += deck_card_qty
    this_deck = Deck(deck_file, deck_dict, {'tag': 'anything'})
    this_deck.update_missing_cards(card_inv_dict)
    decks.append(this_deck)

for deck in decks:
    for card_name, missing_qty in deck.deck_missing_cards.items():
        if card_name not in most_needed_cards:
            most_needed_cards[card_name] = 0
        most_needed_cards[card_name] += missing_qty

# Do collection filtering, based on whatever criteria I want
filtered_list = item_list.copy()
#Filter by set
chosen_set, filtered_list = sort_and_filter(filtered_list, 4)

# Filter by card_color
chosen_color, filtered_list = sort_and_filter(filtered_list, 3)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 2)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

# Get W-L structures working
opp_wl_dict = {}
my_prop_wl = {}
opp_prop_wl = {}
w_l_val = [0, 0]  # [wins, losses]
for game_line in game_wl:
    my_prop, opp_prop, opp_name, w_l = game_line.split(';')

    # Validate WL Data
    if opp_name not in opp_wl_dict:
        opp_wl_dict[opp_name] = [0, 0]
    if my_prop not in my_prop_wl:
        my_prop_wl[my_prop] = [0, 0]
    if opp_prop not in opp_prop_wl:
        opp_prop_wl[opp_prop] = [0, 0]

    if w_l not in ['W', 'L']:
        print(f"Invalid W/L value {w_l} in W-L data")
        continue
    if w_l == 'W':
        w_l_val[0] += 1
        my_prop_wl[my_prop][0] += 1
        opp_prop_wl[opp_prop][0] += 1
        opp_wl_dict[opp_name][0] += 1
    else:
        w_l_val[1] += 1
        my_prop_wl[my_prop][1] += 1
        opp_prop_wl[opp_prop][1] += 1
        opp_wl_dict[opp_name][1] += 1

games_by_property = {}
for prop, prop_wl in my_prop_wl.items():
    games_by_property[prop] = prop_wl[0] + prop_wl[1]

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/XXXXX Out.txt", 'w', encoding="UTF-8")

    double_print("XXXXX Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    SUGG_STRING = f"Buy {picked_item[1]} ({chosen_color + ' ' + chosen_type}) from " + \
        f"{chosen_set} (have {picked_item[-2]} out of {picked_item[-1]})"
    double_print(SUGG_STRING, out_file_h)

    double_print("\nMost needed cards:", out_file_h)
    sorted_most_needed = sorted(most_needed_cards.items(), key=lambda x: (-x[1], x[0]))
    for card_name, needed_qty in sorted_most_needed[:10]:
        double_print(f" - {card_name}: {needed_qty} cards", out_file_h)

    sorted_decks = sorted(decks, key=lambda x: x.get_num_missing_cards())
    double_print("\nDecks closest to completion:", out_file_h)
    used_properties = set()
    for deck in sorted_decks:
        if deck.get_num_missing_cards() == 0:
            double_print(f" - Completed deck: {deck.deck_name}", out_file_h)
            continue
        PROCESS_DECK = True
        if deck.deck_tags['property'] in used_properties:
            PROCESS_DECK = False
        if not PROCESS_DECK:
            continue
        used_properties.add(deck.deck_tags['property'])
        double_print(f" - {deck.deck_name}: {deck.get_num_missing_cards()} cards", out_file_h)
        for card_name, missing_qty in sorted(deck.deck_missing_cards.items()):
            CARD_STR = f"    - {card_name}: {missing_qty}"
            double_print(CARD_STR, out_file_h)

    double_print("\nWin-Loss Information:", out_file_h)
    double_print("My record: " + f"{w_l_val[0]}-{w_l_val[1]}", out_file_h)
    double_print("Win-Loss by Property:", out_file_h)
    for prop, wl_vals in sorted(my_prop_wl.items()):
        double_print(f" - {prop}: {wl_vals[0]}-{wl_vals[1]}", out_file_h)

    double_print("Record Against Properties:", out_file_h)
    for prop, wl_vals in sorted(opp_prop_wl.items()):
        double_print(f" - {prop}: {wl_vals[0]}-{wl_vals[1]}", out_file_h)

    double_print("Record Against Opponents:", out_file_h)
    for opp_name, wl_vals in sorted(opp_wl_dict.items()):
        double_print(f" - {opp_name}: {wl_vals[0]}-{wl_vals[1]}", out_file_h)

    out_file_h.close()
