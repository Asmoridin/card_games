#!/usr/bin/python3

"""
Collection manager/purchase suggester for Godzilla. Reads in card data and deck lists, tracks
collection ownership, and suggests cards to acquire based on missing cards in decks and overall
collection needs. Also tracks win-loss records by various categories for strategic insights.
"""

import os

from card_games.General.Libraries.deck import Deck
from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Godzilla"
FILE_PREFIX = os.path.join("card_games", "G", "Godzilla_Card_Game")

# Define valid values for card attributes
valid_colors = ['Red', 'Blue', 'Green', 'White']
valid_rarities = ['C', 'UC', 'R', 'SR', 'SD', 'PRP']
valid_card_types = ['Monster', 'Battle', 'Strategy']
item_list = [] # Where all the cards will end up getting stored

# Set up directory paths
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = os.path.join("G", "Godzilla_Card_Game")
DECK_PREFIX = os.path.join(FILE_PREFIX, "Decks")
DATA_PREFIX = os.path.join(FILE_PREFIX, "Data")

def fix_card_name(in_card_name, correction_dict):
    """
    Handling variant ways that a card name might be written across different data sources
    and standardizing to a single version for consistency.
    """
    if in_card_name in correction_dict:
        return correction_dict[in_card_name]
    return in_card_name

def read_decks(deck_format, use_format_cards):
    """
    Reads in deck lists from the Decks folder, validating card names and quantities, and
    returning a list of dect formats
    """
    decks = []
    format_card_dict = {}
    for card in use_format_cards:
        format_card_dict[card[0]] = card[5]
    for deck_file in os.listdir(os.path.join(DECK_PREFIX, deck_format)):
        if not deck_file.endswith('.txt'):
            print("Skipping non-txt file in decks folder:", deck_file)
            continue
        deck_path = os.path.join(DECK_PREFIX, deck_format, deck_file)
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
            if deck_card_name not in format_card_dict:
                print(f"Unknown card {deck_card_name} in deck {deck_path}")
            if deck_card_name not in deck_dict:
                deck_dict[deck_card_name] = 0
            deck_dict[deck_card_name] += deck_card_qty
        this_deck = Deck(deck_file, deck_dict, {'tag': 'anything'})
        decks.append(this_deck)
    return decks

def aggregate_most_needed(deck_lists):
    """
    From a list of dicts, of cards missing for decks, generate a list of tuples of those cards
    and a total weight of said cards
    """
    ret_list = []
    temp_dict = {}
    for deck_list in deck_lists:
        for deck_card, deck_card_qty in deck_list[2].items():
            if deck_card not in temp_dict:
                temp_dict[deck_card] = 0
            temp_dict[deck_card] += deck_card_qty
    for temp_card, temp_card_qty in temp_dict.items():
        ret_list.append((temp_card, temp_card_qty))
    return ret_list

# Not used in this game
# def parse_restrictions(restr_lines):
#     """
#     Create a list of restrictions for each card, if relevant
#     """
#     return_dict = {}
#     return return_dict

def in_format(_in_card, _format_name):
    """
    Given a card and a format, determine if the card is legal in that format
    """
    return True

def process_formats(format_name, _=None, find_unused=False):
    """
    Given a format_name, process everything we need- find the suggested card, give stats on 
    the format, and parse, and sort the various decks.
    """
    # Dictionary of formats to corresponding directory
    format_dict = {
        'Standard': 'Standard',
    }

    return_dict = {}
    return_dict['FILTERED'] = {}
    format_card_list = []
    format_own = 0
    format_total = 0
    for in_card in item_list:
        if in_format(in_card, format_name):
            format_card_list.append(in_card)
            format_total += in_card[-1]
            format_own += in_card[-2]
    format_cards = len(format_card_list)
    FORMAT_LIST.append((format_name, format_own, format_total))

    return_dict['FILTERED']['set'], ft_filtered_list = \
        sort_and_filter(format_card_list, 8, by_len = True)
    return_dict['FILTERED']['color'], ft_filtered_list = sort_and_filter(ft_filtered_list, 2)
    return_dict['FILTERED']['type'], ft_filtered_list = sort_and_filter(ft_filtered_list, 3)
    return_dict['FILTERED']['name'], ft_filtered_list = sort_and_filter(ft_filtered_list, 0)
    return_dict['ITEM'] = ft_filtered_list[0]

    format_decks = read_decks(format_dict[format_name], format_card_list)

    if find_unused:
        used_cards = set()
        for check_deck in format_decks:
            for check_card_name in check_deck.deck_cards:
                used_cards.add(check_card_name)
        unused_cards = []
        for card_row in format_card_list:
            if card_row[0] not in used_cards:
                unused_cards.append((card_row[0], card_row[5]))
        return_dict['UNUSED'] = unused_cards

    format_decks_minus_own = []
    for work_deck in format_decks:
        work_deck.update_missing_cards(card_inv_dict)
        format_decks_minus_own.append((work_deck.deck_name, work_deck.get_num_missing_cards(),
            work_deck.deck_missing_cards))

    format_most_needed = aggregate_most_needed(format_decks_minus_own)
    format_most_needed = sorted(format_most_needed, key=lambda x:(-1 * x[1], x[0]))
    format_decks_minus_own = sorted(format_decks_minus_own, key=lambda x:x[1])
    return_dict['FORMAT_OWN'] = format_own
    return_dict['FORMAT_TOTAL'] = format_total
    return_dict['FORMAT_CARDS'] = format_cards
    return_dict['DECKS'] = format_decks_minus_own
    return_dict['NEEDED'] = format_most_needed
    return return_dict

def get_max_rarity(rarity_list, rarity_order):
    """
    Given a list of rarities, return the max rarity, where 
    Mythic Rare > Rare > Uncommon > Common > Land
    """
    return max(rarity_list, key=rarity_order.index)

def handle_output(format_name, format_dict, dest_fh):
    """
    Handle the output, so I don't have to do this multiple times
    """
    double_print(f"\n*** {format_name.upper()} ***", dest_fh)

    tot_str = f"There are {format_dict['FORMAT_CARDS']} {format_name} legal cards"
    double_print(tot_str, dest_fh)

    summ_str = f"Have {format_dict['FORMAT_OWN']} out of {format_dict['FORMAT_TOTAL']} - " + \
        f"{100* format_dict['FORMAT_OWN']/format_dict['FORMAT_TOTAL']:.2f} percent of a playset"
    double_print(summ_str, dest_fh)

    purch_str = f"Chosen card is a(n) {format_dict['FILTERED']['type']} from " + \
        f"{format_dict['FILTERED']['set']} - {format_dict['FILTERED']['name']}. I own " + \
        f"{format_dict['ITEM'][-2]} of {format_dict['ITEM'][-1]}"
    double_print(purch_str, dest_fh)

    if 'UNUSED' in format_dict:
        rarity_sort_order = ['Common', 'Uncommon', 'Rare']
        # Sort unused dict by rarity (Mythic Rare > Rare > Uncommon > Common > Land)
        format_dict['UNUSED'] = sorted(format_dict['UNUSED'],
                key=lambda x: rarity_sort_order.index(get_max_rarity(x[1], rarity_sort_order)),
                    reverse=True)
        rarity_string = f"\nUnused card with highest rarity is: {format_dict['UNUSED'][0][0]} " + \
            f"({sorted(format_dict['UNUSED'][0][1])})"
        double_print(rarity_string , dest_fh)

    if len(format_dict['DECKS']) != 0:
        double_print(f"\nClosest deck to completion ({format_dict['DECKS'][0][0]}) is at " + \
            f"{format_dict['DECKS'][0][1]} cards.", dest_fh)
        double_print(str(format_dict['DECKS'][0][2]), dest_fh)

        double_print("\nMost needed cards are:", dest_fh)
        for pr_card_tuple in format_dict['NEEDED'][:10]:
            double_print(f" - {pr_card_tuple[0]}: {pr_card_tuple[1]}", dest_fh)

# Pull in card data
with open(os.path.join(DATA_PREFIX, "Godzilla Card List.txt"), 'r', encoding="UTF-8") as file_h:
    lines = file_h.readlines()
lines = [line.strip() for line in lines]

# Pull in additional data files, and set up data structures
with open(os.path.join(DATA_PREFIX, "Godzilla Sets.txt"), 'r', encoding="UTF-8") as in_sets:
    game_sets = in_sets.readlines()
game_sets = [line.strip() for line in game_sets if line.strip() != '']

with open(os.path.join(DATA_PREFIX, "Godzilla WL Data.txt"), 'r', encoding="UTF-8") as in_wl:
    game_wl = in_wl.readlines()
game_wl = [line.strip() for line in game_wl if line.strip() != '']

# Read in the card data, validating and organizing as we go. Track total ownership and max
# for collection completion percentage.
TOTAL_OWN = 0
TOTAL_MAX = 0
card_inv_dict = {}
most_needed_cards = {}
card_ids = set()
for line in lines:
    if line == '' or line.startswith('#'):
        continue

    CARD_MAX = 4
    temp_max = 0
    line_vals = line.split(';')

    if len(line_vals) == 10:
        card_name, card_id, card_colors, card_type, card_rarities, card_traits, card_level, \
            card_invasion, card_sets, card_own = line_vals
    elif len(line_vals) == 11:
        card_name, card_id, card_colors, card_type, card_rarities, card_traits, card_level, \
            card_invasion, card_sets, card_own, temp_max = line_vals
    else:
        print("Invalid line:")
        print(line)
        continue

    # Validate card data
    if card_id in card_ids:
        print(f"Duplicate card ID: {card_id}")
    card_ids.add(card_id)
    card_sets = card_sets.split('/')
    for card_set in card_sets:
        if card_set not in game_sets:
            print(f"Unknown set {card_set} for {card_name} ({card_id})")
    if card_type not in valid_card_types:
        print(f"Invalid card type {card_type} for {card_name}")
    for card_color in card_colors.split('/'):
        if card_color not in valid_colors:
            print(f"Invalid card color {card_color} for {card_name} ({card_id})")
    card_rarities = card_rarities.split('/')
    for card_rarity in card_rarities:
        if card_rarity not in valid_rarities:
            print(f"Invalid card rarity {card_rarity} for {card_name} ({card_id})")

    card_own = int(card_own)
    if temp_max != 0:
        CARD_MAX = int(temp_max)

    # With card data now validated, populate our structures
    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    if card_own < CARD_MAX:
        most_needed_cards[card_name] = CARD_MAX - card_own
    card_inv_dict[card_name] = card_own
    item_list.append((card_name, card_id, card_colors, card_type, card_rarities, card_traits, \
            card_level, card_invasion, card_sets, card_own, CARD_MAX))

# Get W-L structures working
opp_wl_dict = {} # opp -> race -> ambassador -> [wins, total_games]
my_race_wl = {} # race -> ambassador -> [wins, total_games]
all_race_wl = {} # total of how many times I've seen a race, and they've won
w_l_val = [0, 0]  # [wins, total_games]
for game_line in game_wl:
    line_vals = game_line.split(';')
    my_race = line_vals[0]
    my_ambassador = line_vals[1]
    game_winner = line_vals[-1]
    opponent_info = line_vals[2:-1]
    # Determine if opponent_info is valid, should be mod 3
    if len(opponent_info) % 3 != 0:
        print(f"Invalid opponent info in W-L data: {opponent_info}")
        continue
    # Now break those opponent infos into tuples of
    # (opponent name, opponent race, and opponent ambassador)
    opponent_info = [tuple(opponent_info[i:i+3]) for i in range(0, len(opponent_info), 3)]

    w_l_val[1] += 1
    if my_race not in my_race_wl:
        my_race_wl[my_race] = {}
    if my_ambassador not in my_race_wl[my_race]:
        my_race_wl[my_race][my_ambassador] = [0, 0]
    my_race_wl[my_race][my_ambassador][1] += 1

    for opp_tuple in opponent_info:
        opp_name, opp_race, opp_ambassador = opp_tuple
        if opp_name not in opp_wl_dict:
            opp_wl_dict[opp_name] = {}
        if opp_race not in all_race_wl:
            all_race_wl[opp_race] = [0, 0]
        if opp_race not in opp_wl_dict[opp_name]:
            opp_wl_dict[opp_name][opp_race] = {}
        if opp_ambassador not in opp_wl_dict[opp_name][opp_race]:
            opp_wl_dict[opp_name][opp_race][opp_ambassador] = [0, 0]
    if game_winner not in opp_wl_dict and game_winner != 'Me':
        print(f"Unknown winner in W-L data: {game_winner}")
        continue
    # Validate WL Data
    if my_race not in my_race_wl:
        my_race_wl[my_race] = [0, 0]
    if game_winner == 'Me':
        w_l_val[0] += 1
        my_race_wl[my_race][my_ambassador][0] += 1
        for opp_tuple in opponent_info:
            opp_wl_dict[opp_tuple[0]][opp_tuple[1]][opp_tuple[2]][1] += 1
            all_race_wl[opp_tuple[1]][1] += 1
        all_race_wl[my_race][0] += 1
    else:
        for opp_tuple in opponent_info:
            if opp_tuple[0] == game_winner:
                opp_wl_dict[opp_tuple[0]][opp_tuple[1]][opp_tuple[2]][0] += 1
                all_race_wl[opp_tuple[1]][0] += 1
            opp_wl_dict[opp_tuple[0]][opp_tuple[1]][opp_tuple[2]][1] += 1
            all_race_wl[opp_tuple[1]][1] += 1

FORMAT_LIST = []

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/Godzilla Out.txt", 'w', encoding="UTF-8")

    double_print("Godzilla Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    # Standard
    standard_dict = process_formats("Standard")
    handle_output("Standard", standard_dict, out_file_h)

    double_print("\nPercentages ordered by format:", out_file_h)
    FORMAT_LIST = sorted(FORMAT_LIST, key=lambda x:(x[1]/x[2], x[0]), reverse=True)
    for print_format in FORMAT_LIST:
        double_print(f"{print_format[0]}: {100 * print_format[1]/print_format[2]:.2f}", out_file_h)

    double_print("\nWin-Loss Information:", out_file_h)
    double_print("My record: " + f"{w_l_val[0]} wins, {w_l_val[1]} games", out_file_h)

    double_print("Record Against Opponents:", out_file_h)
    print(opp_wl_dict)
    for opp_name, play_info in sorted(opp_wl_dict.items()):
        print(opp_name)
        print(play_info)
    print("All Races")
    print(my_race_wl)
    print("My Races")
    print(all_race_wl)
    out_file_h.close()
