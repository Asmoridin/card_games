#!/usr/bin/python3

"""
Inventory manager and collection suggestor for the WARS TCG 
"""

import os
from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter
from steve_utils.check_inventory import check_inventory

GAME_NAME = "WARS TCG"

CARD_SETS = ['Incursion', 'Nowhere to Hide']
VALID_CARD_TYPES = ['Ship', 'Interrupt', 'Character', 'Asset', 'Location', 'Order', 'Weapon',
    'Vehicle', 'Nobot']
VALID_AFFILIATIONS = ['Maverick', 'Quay', 'Earther', 'Independent', 'Shi', 'Gongen', ]

if os.getcwd().endswith('card_games'):
    file_h = open('DB/WARSTCGData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'Decks/WARS TCG'
else:
    file_h = open('card_games/DB/WARSTCGData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'card_games/Decks/WARS TCG'

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

card_names = set()

def read_decks():
    """
    Takes in a format, and returns a list of Deck dicts
    """
    ret_list = []
    for deck_filename in os.listdir(DECK_DIR):
        deck_qty = 0
        deck_fh = open(DECK_DIR + "/" + deck_filename, 'r', encoding="UTF-8")
        deck_lines = deck_fh.readlines()
        deck_fh.close()
        deck_lines = [line.strip() for line in deck_lines]
        this_deck = {}
        for deck_line in deck_lines:
            if deck_line == '' or deck_line.startswith('#'):
                continue
            deck_line = deck_line.replace(' (starting)', '')
            try:
                deck_card_qty = int(deck_line.split(' ')[0])
            except ValueError:
                print(f"Error in deck: {deck_filename}")
                print(deck_line)
                continue
            deck_card_name = ' '.join(deck_line.split(' ')[1:]).strip()
            if deck_card_name == 'Talkan':
                print(f"Talkan is banned, but in deck {deck_filename}")
            deck_qty += deck_card_qty
            if deck_card_name not in this_deck:
                this_deck[deck_card_name] = 0
            this_deck[deck_card_name] += deck_card_qty
        ret_list.append({'name':deck_filename, 'list':this_deck})
        if deck_qty != 60:
            print(f"Deck {deck_filename} doesn't have 60 cards ({deck_qty}).")
    return ret_list

def check_decks(list_of_decks, list_of_cards):
    """
    Given:
    - a list of deck objects, and a list of relevant card tuples
    Return:
    - a list of tuples that are [DECK_NAME], [MISSING_NO], [MISSING_CARDS]
    """
    inventory_dict = {}
    for in_card in list_of_cards:
        inventory_dict[in_card[0]] = in_card[5]

    ret_list = check_inventory(list_of_decks, inventory_dict)
    return ret_list

TOTAL_MAX = 0
TOTAL_OWN = 0
card_lines = []
card_list = []
card_qty_dict = {}
for line in lines:
    if line == '' or line.startswith('#'):
        continue

    try:
        card_name, card_set, rarity, card_affil, card_type, max_card, card_own = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if card_name in card_names:
        print("Duplicate card name: " + card_name)
    card_names.add(card_name)
    if card_set not in CARD_SETS:
        print(f"Invalid card set of {card_set} for {card_name}")
    card_type = card_type.split()[0].lower().capitalize()
    if card_type not in VALID_CARD_TYPES:
        print(f"Invalid card type of {card_type} for {card_name}")
    if card_affil not in VALID_AFFILIATIONS:
        print(f"Invalid card affiliation of {card_affil} for {card_name}")
    max_card = int(max_card)
    card_own = int(card_own)
    TOTAL_MAX += max_card
    TOTAL_OWN += card_own
    card_qty_dict[card_name] = card_own
    card_list.append((card_name, card_set, rarity, card_affil, card_type, card_own, max_card))


# Sort/filter by card set
chosen_set, filtered_lines = sort_and_filter(card_list, 1)
# Affiliaton
chosen_affil, filtered_lines = sort_and_filter(filtered_lines, 3)
# Card Type
chosen_card_type, filtered_lines = sort_and_filter(filtered_lines, 4)
# Rarity
_, filtered_lines = sort_and_filter(filtered_lines, 2)
# Find a final card to go with
chosen_card, filtered_lines = sort_and_filter(filtered_lines, 0)
final_card = filtered_lines[0]

if __name__ == "__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("output/WARSTCGOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/output/WARSTCGOut.txt", 'w', encoding="UTF-8")

    double_print("WARS TCG Inventory Tracker\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)
    double_print(f"Buy a {chosen_affil} from {chosen_set}, maybe {chosen_card} (have " + \
        f"{final_card[5]} out of {final_card[6]})\n", out_file_h)

    # Read in the decks
    decks = []
    decks = read_decks()

    deck_missing_list = check_decks(decks, card_list)

    deck_missing_list = sorted(deck_missing_list, key=lambda x:(x[1], x[0]))
    lowest_deck = deck_missing_list[0]
    double_print(f"\nClosest deck to completion is {lowest_deck[0]}, needing just " + \
        f"{lowest_deck[1]} cards:", out_file_h)
    double_print(str(lowest_deck[2]), out_file_h)

    most_needed_cards = {}
    for deck in deck_missing_list:
        for needed_card_name, needed_card_qty in deck[2].items():
            if needed_card_name not in most_needed_cards:
                most_needed_cards[needed_card_name] = 0
            most_needed_cards[needed_card_name] += needed_card_qty
    most_needed_cards_tuple = [(k,v) for k, v in most_needed_cards.items()]
    most_needed_cards_tuple = sorted(most_needed_cards_tuple, key = lambda x:(-1 * x[1], x[0]))

    double_print("\nTop ten most needed cards: ", out_file_h)
    for most_needed_name, most_needed_qty in most_needed_cards_tuple[:10]:
        double_print(f"{most_needed_name} - {most_needed_qty}", out_file_h)
