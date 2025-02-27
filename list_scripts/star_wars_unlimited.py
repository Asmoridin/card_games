#!/usr/bin/python3

"""
Collection tracker/purchase recommender for the Star Wars Unlimited card game.
"""

import os

from steve_utils.output_utils import double_print
from steve_utils.sort_and_filter import sort_and_filter

GAME_NAME = "Star Wars: Unlimited"

valid_types = ['Leader', 'Base', 'Ground Unit', 'Space Unit', 'Event', 'Upgrade']
card_rarities = {'C':'Common', 'U':'Uncommon', 'R': 'Rare', 'S':'Special', 'L':'Legendary'}
card_colors_map = {'U':'Blue', 'B':'Black', 'R':'Red', 'G':'Green',
                   'W':'White', 'Y':'Yellow', 'N':'Neutral'}

def process_card_set(card_set_in):
    """
    Given a string of card set information, process it into list, and return them.
    """
    ret_list = []
    ret_card_sets = []
    ret_card_rarities = []
    for card_printing in card_set_in.split('/'):
        try:
            check_card_set, _, card_rarity = card_printing.split('-')
        except ValueError:
            print(f"Faulty set line: {card_printing}")
            return [[], []]
        if check_card_set == 'SOR':
            check_card_set = 'Spark of Rebellion'
        elif check_card_set == 'SHD':
            check_card_set = 'Shadows of the Galaxy'
        elif check_card_set == 'TWI':
            check_card_set = 'Twilight of the Republic'
        elif check_card_set == 'JTL':
            check_card_set = 'Jump to Lightspeed'
        else:
            print(f"Unknown card set {check_card_set}")
            return [[], []]

        if card_rarity in card_rarities:
            card_rarity = card_rarities[card_rarity]
        else:
            print(f"Unknown card rarity {card_rarity}")
            return []

        ret_card_sets.append(check_card_set)
        ret_card_rarities.append(card_rarity)
    ret_list = [ret_card_sets, ret_card_rarities]
    return ret_list

def convert_colors(in_color):
    """
    Takes in a string, and then returns a list of card colors for this card
    """
    ret_list = []
    for color_code in in_color.split('/'):
        if color_code in card_colors_map:
            ret_list.append(card_colors_map[color_code])
        else:
            print(f"Unknown color {color_code}")
            return []
    return ret_list

def parse_deck(deck_lines, collection_dict_in):
    """
    Take a list of lines from a deck that has een read in, and convert the lines
    into an output dictionary
    """
    ret_dict = {}
    for deck_line in deck_lines:
        deck_line = deck_line.strip()
        if deck_line.startswith('//') or deck_line == '':
            continue
        cards_needed, this_card_name = deck_line.split("\t")
        cards_needed = int(cards_needed)
        if this_card_name not in collection_dict_in:
            print("Unknown card: " + this_card_name)
        if this_card_name not in ret_dict:
            ret_dict[this_card_name] = cards_needed
        else:
            ret_dict[this_card_name] += cards_needed
    return ret_dict

def determine_missing(deck_dict, collection_dict_in):
    """
    Given a dictionary for a deck, return what cards I am missing
    """
    ret_dict = {}
    for card, deck_card_qty in deck_dict.items():
        if collection_dict_in[card] < deck_card_qty:
            ret_dict[card] = deck_card_qty - collection_dict_in[card]
    return ret_dict

if os.getcwd().endswith('card_games'):
    file_h = open('DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'Decks/StarWarsUnlimited'
else:
    file_h = open('card_games/DB/StarWarsUnlimitedData.txt', 'r', encoding="UTF-8")
    DECK_DIR = 'card_games/Decks/StarWarsUnlimited'

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

item_list = []
TOTAL_MAX = 0
TOTAL_OWN = 0
collection_dict = {}
full_collection = {}
card_need_dict = {}
card_names = set()
KEEP_READ = True

hyperfoil_list = []
HYPER_MAX = 0
HYPER_OWN = 0

for line in lines:
    if line == '' or line.startswith('#'):
        continue
    if line == "** END **":
        KEEP_READ = False
    if not KEEP_READ:
        continue
    HYPER_OWNED = 0
    if line.count('#') > 0:
        card_printings = line.split('#')[1].split(',')
        for card_style in card_printings:
            try:
                print_qty, print_type = card_style.strip().split(' ')
            except ValueError:
                print("Something up with:")
                print(line)
                continue
            print_qty = int(print_qty)
            if print_type not in ['foil', 'hyperspace', 'hyperfoil', 'showcase']:
                print(f"\nInvalid printing {print_type}")
                print(line)
            if print_type in ['hyperfoil', 'showcase']:
                HYPER_OWNED += 1

    line = line.split('#')[0].strip() # Clears comments on lines
    CARD_MAX = 3
    try:
        if line.count(';') == 4:
            card_name, card_set_info, card_type, card_colors, card_owned = line.split(';')
        else:
            card_name, card_set_info, card_type, card_colors, card_owned, temp_max = line.split(';')
            CARD_MAX = int(temp_max)
    except ValueError:
        print("Following line isn't formatted correctly:")
        print(line)
        continue
    if card_name in card_names:
        print(f"Duplicate card name: {card_name}")
    card_names.add(card_name)
    this_card_sets, this_card_rarities = process_card_set(card_set_info) # pylint: disable=unbalanced-tuple-unpacking

    if card_type not in valid_types:
        print(f"Invalid card type {card_type}")
        continue
    card_colors = convert_colors(card_colors)
    if not card_colors:
        continue

    card_owned = int(card_owned)

    if card_type in ['Leader', 'Base']:
        CARD_MAX = 1
    if card_owned > CARD_MAX:
        CARD_MAX = card_owned
    collection_dict[card_name] = card_owned
    full_collection[card_name] = CARD_MAX

    TOTAL_MAX += CARD_MAX
    TOTAL_OWN += card_owned
    item_list.append((card_name, this_card_sets, this_card_rarities, card_type, card_colors,
        card_owned, CARD_MAX))

    HAS_HYPER = True
    if card_type == 'Base':
        if this_card_rarities == ['Common']:
            HAS_HYPER = False

    if HAS_HYPER:
        HYPER_MAX += 1
        HYPER_OWN += HYPER_OWNED
        hyperfoil_list.append((card_name, this_card_sets, this_card_rarities, card_type,
            card_colors, HYPER_OWNED, 1))

done_decks = []
MIN_DECK_SIZE = 50
MIN_DECK_CARDS = {}
MIN_DECK_NAME = ""
for file_name in os.listdir(DECK_DIR):
    this_deck_file = DECK_DIR + "/" + file_name
    deck_file_h = open(this_deck_file, 'r', encoding="UTF-8")
    this_deck_lines = deck_file_h.readlines()
    deck_file_h.close()
    this_deck_dict = parse_deck(this_deck_lines, collection_dict)
    missing_cards = determine_missing(this_deck_dict, collection_dict)
    if len(missing_cards) == 0:
        done_decks.append(file_name)
    else:
        if len(missing_cards) < MIN_DECK_SIZE:
            MIN_DECK_SIZE = len(missing_cards)
            MIN_DECK_NAME = file_name
            MIN_DECK_CARDS = missing_cards
    for missing_card, missing_card_qty in missing_cards.items():
        if missing_card not in card_need_dict:
            card_need_dict[missing_card] = 0
        card_need_dict[missing_card] += missing_card_qty

missing_full_cards = determine_missing(full_collection, collection_dict)
for missing_card, missing_card_qty in missing_full_cards.items():
    if missing_card not in card_need_dict:
        card_need_dict[missing_card] = 0
    card_need_dict[missing_card] += missing_card_qty

card_need_sorter = []
for card_name, card_qty in card_need_dict.items():
    card_need_sorter.append((card_name, card_qty))
card_need_sorter = sorted(card_need_sorter, key=lambda x:(-1 * x[1], x[0]))

# Filter by set
chosen_set, filtered_list = sort_and_filter(item_list, 1)

# Filter by color
chosen_color, filtered_list = sort_and_filter(filtered_list, 4)

# Filter by card type
chosen_type, filtered_list = sort_and_filter(filtered_list, 3)

# Filter by rarity
chosen_rarity, filtered_list = sort_and_filter(filtered_list, 2)

# Pick a card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

# Hyperfoil filtering
hyper_set, hyper_f_list = sort_and_filter(hyperfoil_list, 1)
hyper_color, hyper_f_list = sort_and_filter(hyper_f_list, 4)
hyper_type, hyper_f_list = sort_and_filter(hyper_f_list, 3)
hyper_rarity, hyper_f_list = sort_and_filter(hyper_f_list, 2)
hyper_card, hyper_f_list = sort_and_filter(hyper_f_list, 0)
hyper_item = hyper_f_list[0]

if __name__=="__main__":
    if os.getcwd().endswith('card_games'):
        out_file_h = open("output/StarWarsUnlimited.txt", 'w', encoding="UTF-8")
    else:
        out_file_h = open("card_games/output/StarWarsUnlimited.txt", 'w', encoding="UTF-8")

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    next_buy_string = f"Buy a {chosen_color} {chosen_type} from {chosen_set} - perhaps " + \
        f"{picked_item[0]} (have {picked_item[5]} out of {picked_item[6]})"
    double_print(next_buy_string, out_file_h)

    hyper_string = f"\nHave {HYPER_OWN} out of {HYPER_MAX} hyperfoil cards - " + \
        f"{100* HYPER_OWN/HYPER_MAX:.2f} percent"
    double_print(f"{hyper_string}", out_file_h)
    hyper_buy_string = f"Buy a {hyper_color} {hyper_type} from {hyper_set} - perhaps " + \
        f"{hyper_item[0]} (have {hyper_item[5]} out of {hyper_item[6]})"
    double_print(hyper_buy_string, out_file_h)

    double_print(f"\nNeed the ({MIN_DECK_SIZE}) following cards to finish the next closest " + \
        f"deck ({MIN_DECK_NAME})", out_file_h)
    double_print(str(list(MIN_DECK_CARDS.items())), out_file_h)

    double_print("\nFollowing decks I own all of the cards for:", out_file_h)
    double_print(", ".join(done_decks), out_file_h)

    double_print("\nMost needed cards:", out_file_h)
    for card_tuple in card_need_sorter[:10]:
        double_print(f"{card_tuple[0]}: {card_tuple[1]}", out_file_h)

    out_file_h.close()
