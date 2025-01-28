#!/usr/bin/python3

"""
Inventory manager and collection suggestor for ST2E card game
"""

import os
from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "Star Trek: Second Edition"

physical_sets = ['Necessary Evil', 'Energize', 'What You Leave Behind', 'Second Edition',
    'Call to Arms', 'Tenth Anniversary Collection', 'Fractured Time', 'Reflections 2.0',
    'Archive Portrait', 'Strange New Worlds', 'To Boldly Go', 'Dangerous Missions',
    "Captain's Log", 'Genesis', 'These Are The Voyages', 'In A Mirror Darkly',
    'What You Leave Behind']
VALID_CARD_TYPES = ['Personnel', 'Ship', 'Dilemma', 'Equipment', 'Event', 'Interrupt', \
    'Mission', ]
VALID_AFFILIATIONS = ['Federation', 'Vidiian', 'Non-Aligned', 'Klingon', 'Romulan', 'Starfleet',
    'Dominion', 'Ferengi', 'Bajoran', 'Cardassian', 'Borg', ]

if os.getcwd().endswith('card_games'):
    file_h = open('DB/StarTrek2EData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'Decks/ST2E'
else:
    file_h = open('card_games/DB/StarTrek2EData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'card_games/Decks/ST2E'

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

card_names = set()

def read_in_deck(in_deck_lines):
    """
    Take a bunch of lines from a deck file, return a dictionary of the deck
    """
    ret_dict = {}
    in_deck_lines = [in_line.strip() for in_line in in_deck_lines]
    in_deck_lines = [in_line.replace('•', '').replace('\t', ' ') for in_line in in_deck_lines]
    for read_line in in_deck_lines:
        if read_line in VALID_CARD_TYPES:
            continue
        if read_line in VALID_AFFILIATIONS:
            continue
        if read_line in ['', 'Missions', 'Headquarters', 'Planet', 'Space', 'Dual']:
            continue
        if read_line.startswith('Dilemma Pile (') or read_line.startswith('Draw Deck ('):
            continue

        try:
            _, deck_card = read_line.split('  ')
        except ValueError:
            print("Potentially invalid line:")
            print(read_line)
            continue

        deck_card_name = ' '.join(deck_card.split(' ')[1:])
        try:
            deck_qty = int(deck_card.split(' ')[0].replace('x', ''))
        except ValueError: # Happens with Missions
            deck_qty = 1
            deck_card_name = deck_card
        if deck_card_name not in card_names:
            print("Invalid card name?: " + deck_card_name)

        if deck_card_name not in ret_dict:
            ret_dict[deck_card_name] = 0
        ret_dict[deck_card_name] += deck_qty
    return ret_dict

def get_missing_cards(in_deck, in_card_dict):
    """
    Given a deck, and a list of owned cards, return a dict of cards missing
    """
    ret_dict = {}
    missing_qty = 0
    for in_card_name, deck_card_qty in in_deck[1].items():
        if in_card_dict[in_card_name] < deck_card_qty:
            missing_qty += deck_card_qty - in_card_dict[in_card_name]
            ret_dict[in_card_name] = deck_card_qty - in_card_dict[in_card_name]
    return(missing_qty, ret_dict)

TOTAL_MAX = 0
TOTAL_OWN = 0
card_lines = []
card_list = []
card_qty_dict = {}
for line in lines:
    if line == '':
        continue

    line = line.split('//')[0].strip()
    try:
        card_name, rarity, card_type, card_affil, card_set, print_type, max_card, \
            card_own = line.split(';')
    except ValueError:
        print("Problem with line:")
        print(line)
        continue
    if card_name in card_names:
        print("Duplicate card name: " + card_name)
    card_names.add(card_name)
    rarity = rarity.split('/')
    for in_rarity in rarity:
        if in_rarity not in ['C', 'U', 'R', 'S', 'P', 'VP', 'V', 'B', 'AP', ]:
            print(f"Invalid rarity of {in_rarity} for {card_name}")
    if card_type not in VALID_CARD_TYPES:
        print(f"Invalid card type of {card_type} for {card_name}")
    if print_type not in ['Print', 'Virtual', 'Both']:
        print(f"Invalid print type of {print_type} for {card_name}")
    card_set = card_set.split('/')
    max_card = int(max_card)
    card_own = int(card_own)
    TOTAL_MAX += max_card
    TOTAL_OWN += card_own
    card_qty_dict[card_name] = card_own
    card_list.append((print_type, card_set, card_type, card_affil, rarity, card_name, \
        card_own, max_card))

print_type_map = {'Print':[0,0], 'Virtual':[0,0]}
# Sort by print type
for line in card_list:
    print_type = line[0]
    if print_type in ['Print', 'Virtual']:
        print_type_map[print_type][0] += line[7]
        print_type_map[print_type][1] += line[6]
    if print_type == 'Both':
        print_type_map['Print'][0] += line[7]
        print_type_map['Print'][1] += line[6]
        print_type_map['Virtual'][0] += line[7]
        print_type_map['Virtual'][1] += line[6]
print_type_sorter = []
for print_type, print_qties in print_type_map.items():
    QTY_HAVE = print_qties[1]
    QTY_TOTAL = print_qties[0]
    print_type_sorter.append((print_type, QTY_HAVE/QTY_TOTAL, QTY_TOTAL - QTY_HAVE))
print_type_sorter = sorted(print_type_sorter, key=lambda x:(x[1], -x[2], x[0]))

new_filter_lines = []
for line in card_list:
    if line[0] == print_type_sorter[0][0] or line[0] == 'Both':
        new_filter_lines.append(line)
filter_lines = new_filter_lines

# Sort/filter by card set
chosen_set, filtered_lines = sort_and_filter(filter_lines, 1)

# Sort by card type, and filter by card set
chosen_card_type, filtered_lines = sort_and_filter(filtered_lines, 2)

# For certain type, sort/filter by affiliation
if chosen_card_type == 'Ship' or chosen_card_type == 'Personnel':
    chosen_affil, filtered_lines = sort_and_filter(filtered_lines, 3)
    #print(chosen_affil)

# Find a final card to go with
chosen_card, filtered_lines = sort_and_filter(filtered_lines, 5)
final_card = filtered_lines[0]

if __name__ == "__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("output/ST2EOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/output/ST2EOut.txt", 'w', encoding="UTF-8")

    double_print("Star Trek 2E CCG Inventory Tracker\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)
    double_print(f"Buy a {final_card[2]} from {chosen_set}, maybe {final_card[5]} (have " + \
        f"{final_card[6]} out of {final_card[7]})", out_file_h)

    # Read in the decks
    decks = []
    for deck_file in os.listdir(DECK_DIR):
        deck_fh = open(DECK_DIR + "/" + deck_file, 'r', encoding="UTF-8")
        deck_lines = deck_fh.readlines()
        deck_fh.close()
        deck_dict = read_in_deck(deck_lines)
        decks.append((deck_file, deck_dict))

    # Create tuple for cards missing from decks (deck_name, missing_card_qty, missing_card_list)
    deck_missing_list = []
    for deck in decks:
        missing_cards = get_missing_cards(deck, card_qty_dict)
        deck_missing_list.append((deck[0], missing_cards[0], missing_cards[1]))

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
