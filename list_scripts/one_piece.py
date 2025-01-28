#!/usr/bin/python3

"""
Collection tracker/management for the One Piece card game
"""

import os
from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "One Piece"

ALL_COLORS = {'U':'Blue', 'G':'Green', 'R':'Red', 'P':'Purple', 'B':'Black', 'Y':'Yellow'}

def validate_colors(in_colors):
    """
    Takes in a string of colors, and returns a list with the full color names
    """
    ret_colors = []
    for color in in_colors.split('/'):
        if color not in ALL_COLORS:
            print("Invalid color: " + color)
        else:
            ret_colors.append(ALL_COLORS[color])
    return ret_colors

if os.getcwd().endswith('card_games'):
    file_h = open('DB/OnePieceData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'Decks/OnePieceTCG'
else:
    file_h = open('card_games/DB/OnePieceData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'card_games/Decks/OnePieceTCG'

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

def parse_deck(deck_lines, collection_dict_in):
    """
    Take a list of lines from a deck that has been read in, and convert the lines
    into an output dictionary
    """
    ret_dict = {}
    for deck_line in deck_lines:
        deck_line = deck_line.strip()
        if deck_line.startswith('#') or deck_line == '':
            continue
        try:
            cards_needed, this_card_number = deck_line.split(" ")
        except ValueError:
            print("Issue with " + deck_line)
            raise
        cards_needed = int(cards_needed)
        if this_card_number not in collection_dict_in:
            print("Unknown card: " + this_card_number)
        if this_card_number not in ret_dict:
            ret_dict[this_card_number] = cards_needed
        else:
            ret_dict[this_card_number] += cards_needed
    return ret_dict

def determine_missing(deck_dict, collection_dict_in):
    """
    Given a dictionary for a deck, return what cards I am missing
    """
    ret_dict = {}
    for this_card, deck_card_qty in deck_dict.items():
        if collection_dict_in[this_card] < deck_card_qty:
            ret_dict[this_card] = deck_card_qty - collection_dict_in[this_card]
    return ret_dict

sub_type_map = {}
TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
dupe_check = set()
NUM_LEADERS = 0
OWN_LEADERS = 0
leaders = {}
collection_dict = {} # Map of card number to owned quantity
card_number_to_name_dict = {} # Map from card numbers to card names
full_collection = {}
card_need_dict = {}
for line in lines:
    if line.startswith('#') or line == '':
        continue
    line = line.split('#')[0]
    try:
        card_name, card_number, card_type, card_color, card_subtypes, card_set, \
            card_own = line.split(';')
    except ValueError:
        print("Possibly invalid line:")
        print(line)
        continue
    if (card_name, card_number) in dupe_check:
        print("Possible duplicate: ")
        print(line)
    dupe_check.add((card_name, card_number))
    try:
        card_own = int(card_own)
    except ValueError:
        print("Invalid line:")
        print(line)
        continue
    if card_subtypes == '':
        print("Missing subtypes:")
        print(line)
        continue
    card_subtypes = card_subtypes.split('/')
    for subtype in card_subtypes:
        if subtype not in sub_type_map:
            sub_type_map[subtype] = 0
        sub_type_map[subtype] += 1
    if card_type not in ['Leader', 'Character', 'Event', 'Stage']:
        print("Invalid card type: " + card_type)
        continue
    card_color = validate_colors(card_color)
    card_set = card_set.split('/')
    collection_dict[card_number] = card_own
    card_number_to_name_dict[card_number] = card_name
    full_collection[card_number] = 4
    CARD_MAX = 4
    if card_type == 'Leader':
        CARD_MAX = 1
        NUM_LEADERS += 1
        OWN_LEADERS += card_own
        leaders[card_number] = (card_name, card_color)
        full_collection[card_number] = 1
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    item_list.append((card_name, card_number, card_type, card_color, card_subtypes, card_set, \
        card_own, CARD_MAX))

deck_tuples = [] # (DeckFile, cards_needed, cards)
for deck_colors in os.listdir(DECK_DIR):
    for file_name in os.listdir(DECK_DIR + "/" + deck_colors):
        CARDS_NEEDED = 0
        THIS_LEADER = ()
        this_deck_file = DECK_DIR + "/" + deck_colors + "/" + file_name
        deck_file_h = open(this_deck_file, 'r', encoding="UTF-8")
        this_deck_lines = deck_file_h.readlines()
        deck_file_h.close()
        this_deck_dict = parse_deck(this_deck_lines, collection_dict)
        for card_num, _ in this_deck_dict.items():
            if card_num in leaders:
                THIS_LEADER = leaders[card_num]
                del leaders[card_num]
        missing_cards = determine_missing(this_deck_dict, collection_dict)
        for card, card_qty in missing_cards.items():
            CARDS_NEEDED += card_qty
        deck_tuples.append((file_name, CARDS_NEEDED, missing_cards, THIS_LEADER))
        for missing_card, missing_card_qty in missing_cards.items():
            if missing_card not in card_need_dict:
                card_need_dict[missing_card] = 0
            card_need_dict[missing_card] += missing_card_qty

missing_full_cards = determine_missing(full_collection, collection_dict)
for missing_card, missing_card_qty in missing_full_cards.items():
    if missing_card not in card_need_dict:
        card_need_dict[missing_card] = 0
    card_need_dict[missing_card] += missing_card_qty

card_sorter = []
for card_number, card_qty in card_need_dict.items():
    card_name = card_number_to_name_dict[card_number]
    card_sorter.append((card_name, card_number, card_qty))
card_sorter = sorted(card_sorter, key=lambda x:(-1 * x[2], x[0], x[1]))

deck_sorter = []
deck_sorter = sorted(deck_tuples, key=lambda x:x[1])

# Filter by subtype
chosen_subtype, filtered_list = sort_and_filter(item_list, 4)

# If there's an available Leader, let's make sure we filter to them.
HAS_LEADER = False
leader_list = []
for card_tuple in filtered_list:
    if card_tuple[2] == 'Leader' and card_tuple[6] == 0:
        HAS_LEADER = True
        leader_list.append(card_tuple)
if HAS_LEADER:
    filtered_list = leader_list

#Filter by color
chosen_color, filtered_list = sort_and_filter(filtered_list, 3)

# Filter by card type
chosen_type, filtered_list = sort_and_filter(filtered_list, 2)

# Filter by set
chosen_set, filtered_list = sort_and_filter(filtered_list, 5)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

singleton_traits = []
for subtype, subtype_count in sub_type_map.items():
    if subtype_count == 1:
        singleton_traits.append(subtype)

if __name__ == "__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("output/OnePieceOut.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/output/OnePieceOut.txt", 'w', encoding="UTF-8")

    double_print("One Piece TCG Inventory Tracker, and purchase suggestion tool\n", out_file_h)

    TRAIT_STR = "Following traits show up only once: " + ', '.join(sorted(singleton_traits))
    double_print(TRAIT_STR, out_file_h)

    SUMMARY_STRING = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(SUMMARY_STRING, out_file_h)

    ldr_str = f"\nThere are {NUM_LEADERS} leaders in the game - I own {OWN_LEADERS}\n"
    double_print(ldr_str, out_file_h)

    double_print(f"Chosen subtype is {chosen_subtype}, chosen color is {chosen_color}", out_file_h)
    double_print(f"Chosen card type: {chosen_type}, and chosen set: {chosen_set}", out_file_h)
    sugg_string = f"Buy {picked_item[0]} (have " + \
        f"{picked_item[6]} out of {picked_item[7]})"
    double_print(sugg_string, out_file_h)

    double_print("\nMost needed cards:", out_file_h)
    for card_tuple in card_sorter[:10]:
        double_print(f"{card_tuple[0]} ({card_tuple[1]}): {card_tuple[2]}", out_file_h)

    if len(leaders) > 0:
        double_print(f"\nMissing decks for leaders: ({len(leaders)})", out_file_h)
        for card_number, card_tuple in sorted(leaders.items(), key=lambda x:(x[1][0], x[0])):
            double_print(f"- {card_tuple[0]} ({card_tuple[1]}), ({card_number})", out_file_h)

    double_print("\nLowest deck: ", out_file_h)
    unused_colors = list(ALL_COLORS.values())
    for check_deck in deck_sorter:
        USE_DECK = True
        for check_color in check_deck[3][1]:
            if check_color not in unused_colors:
                USE_DECK = False
        if USE_DECK:
            double_print(f"\n{check_deck[0]} ({'/'.join(check_deck[3][1])}) - Missing " + \
                f"{check_deck[1]} cards", out_file_h)
            for print_name, print_qty in sorted(check_deck[2].items()):
                this_name = f"{card_number_to_name_dict[print_name]} ({print_name})"
                double_print(f"- {this_name}: {print_qty}", out_file_h)
            for check_color in check_deck[3][1]:
                unused_colors.remove(check_color)

    out_file_h.close()
