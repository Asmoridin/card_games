#!/usr/bin/python3

"""
Inventory tracker and purchase selector for the Star Wars CCG
"""

import os
import re

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Star Wars CCG"

FILE_PREFIX = "card_games/S/Star_Wars_CCG"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "S/Star_Wars_CCG"

file_h = open(FILE_PREFIX + '/Data/StarWarsCCGData.txt', 'r', encoding="UTF-8")
DECK_DIR = FILE_PREFIX + "/Decks"
OUT_FILE_NAME = FILE_PREFIX + "/StarWarsCCGOut.txt"

VALID_CARD_TYPES = ['Character', 'Location', 'Device', 'Effect', 'Interrupt', 'Starship',
    'Vehicle', 'Weapon', 'Creature', 'Epic Event', 'Jedi Test', 'Objective', "Admiral's Order",
    'Podracer', 'Defensive Shield']
VALID_RARITIES = ['R1', 'R2', 'U1', 'U2', 'C1', 'C2', 'C3', 'P', 'F', 'C', 'U', 'R', 'XR', 'UR']

SETS = ['Premiere', 'Premiere Introductory 2-Player Game', 'Rebel Leader Pack', 'Free Jedi Pack',
    'A New Hope', 'Empire Strikes Back Introductory 2-Player Game', 'Hoth', 'Dagobah',
    'Cloud City', "Jabba's Palace", "Official Tournament Sealed Deck", "Special Edition",
    'Enhanced Premiere', 'Endor', 'Enhanced Cloud City', "Enhanced Jabba's Palace",
    'Third Anthology', 'Death Star II', "Jabba's Palace Sealed Deck", 'Reflections II',
    'Tatooine', 'Coruscant', 'Reflections III', 'Theed Palace',]

SET_FOLDER_MAP = {
    'Premiere':'01 - Premiere',
    'A New Hope':'02 - A New Hope',
    'Hoth':'03 - Hoth',
    'Dagobah':'04 - Dagobah',
    'Cloud City':'05 - Cloud City',
    "Jabba's Palace":"06 - Jabba's Palace",
    "Special Edition":'07 - Special Edition',
    'Endor':'08 - Endor',
    'Death Star II':'09 - Death Star II',
}

def parse_sets(this_card_name, set_string):
    """
    Take in a set string, and return a tuple:
    ([sets], [rarites])
    """
    ret_sets = []
    ret_rarities = set()
    for set_part in set_string.split('/'):
        match_obj = re.search(r"(.*) \((.*)\)", set_part)
        if match_obj:
            this_set, this_set_rarity = match_obj.groups()
            if this_set not in SETS:
                print(f"Unknown set: {this_set}")
            if this_set_rarity not in VALID_RARITIES:
                print(f"Unknown rarity: {this_set_rarity}")
            ret_sets.append(this_set)
            ret_rarities.add(this_set_rarity)
        else:
            print("[" + this_card_name + "] Issue with: " + set_part)
    return (ret_sets, list(ret_rarities))

def read_decks(deck_era):
    """
    Takes in a deck era (basically, set), and returns a list of Deck dicts
    """
    ret_list = []
    era_deck_dir = DECK_DIR + "/" + SET_FOLDER_MAP[deck_era]
    for deck_side in os.listdir(era_deck_dir):
        for deck_filename in os.listdir(era_deck_dir + "/" + deck_side):
            deck_name = deck_side + "/" + deck_filename
            deck_fh = open(era_deck_dir + "/" + deck_name, 'r', encoding="UTF-8")
            deck_lines = deck_fh.readlines()
            deck_fh.close()
            deck_lines = [line.strip() for line in deck_lines]
            this_deck = {}
            total_deck_cards = 0
            for deck_line in deck_lines:
                if deck_line == '' or deck_line.startswith('#'):
                    continue
                try:
                    deck_card_qty = int(deck_line.split(' ')[0])
                except ValueError:
                    print("Error in deck:")
                    print(era_deck_dir + "/" + deck_name)
                    print(deck_line)
                    continue
                deck_card_name = ' '.join(deck_line.split(' ')[1:]).strip()
                deck_card_name = deck_card_name.replace(' (starting)', '')
                if deck_card_name not in this_deck:
                    this_deck[deck_card_name] = 0
                this_deck[deck_card_name] += deck_card_qty
                total_deck_cards += deck_card_qty
            if total_deck_cards != 60:
                print(f"Deck {deck_name} may not have correct amount of cards: {total_deck_cards}")
            ret_list.append({'name':deck_name, 'list':this_deck})
    return ret_list

def check_decks(list_of_decks, list_of_cards):
    """
    Given:
    - a list of deck objects, and a list of relevant card tuples
    Return:
    - a list of tuples that are [DECK_NAME], [MISSING_NO], [MISSING_CARDS]
    """

    inventory_dict = {}
    inventory_dict['DS'] = {}
    inventory_dict['LS'] = {}
    card_maxes = {}
    card_maxes['DS'] = {}
    card_maxes['LS'] = {}
    for in_card in list_of_cards:
        inventory_dict[in_card[1]][in_card[0]] = in_card[5]
        card_maxes[in_card[1]][in_card[0]] = in_card[6]
        # Potential card name cleanup
        cleanup_rules = {'ó':'o'}
        clean_name = in_card[0]
        for start_letter, change_letter in cleanup_rules.items():
            clean_name = clean_name.replace(start_letter, change_letter)
        inventory_dict[in_card[1]][clean_name] = in_card[5]

    # Quick check to increase number of cards if higher than what I would consider max
    for deck in list_of_decks:
        check_key = 'LS'
        if deck['name'].startswith('Dark Side'):
            check_key = 'DS'
        for check_card, check_card_qty in deck['list'].items():
            if check_card in card_maxes[check_key]:
                if check_card_qty > card_maxes[check_key][check_card]:
                    print(f"Increase max of {check_card} ({check_key}) to {check_card_qty}")

    ret_list = check_inventory(list_of_decks, inventory_dict)
    return ret_list

def check_inventory(in_lists, inventory_dict):
    """
    Given:
    - a list of dicts, representing decks or army builds
    - a dict, representing the inventory of this product
    Return:
    - a list of tuples that are [LIST_NAME], [MISSING_NO], [MISSING_ITEMS]
    """
    ret_list = []

    for c_item in in_lists:
        use_dict_key = "LS"
        if c_item['name'].startswith('Dark Side'):
            use_dict_key = "DS"
        this_list_missing = 0
        this_list_miss_items = {}
        for item_name, item_count in c_item["list"].items():
            if item_name in inventory_dict[use_dict_key]:
                inventory_amount = inventory_dict[use_dict_key][item_name]
                if item_count > inventory_amount:
                    this_list_missing += item_count - inventory_amount
                    this_list_miss_items[item_name] = item_count - inventory_amount
            else:
                print(f"Missing item ({item_name}) in {c_item['name']}")
                this_list_missing += item_count
                this_list_miss_items[item_name] = item_count
        ret_list.append((c_item["name"], this_list_missing, this_list_miss_items))
    return ret_list

def aggregate_most_needed(deck_lists):
    """
    From a list of dicts, of cards missing for decks, generate a list of tuples of those cards
    and a total weight of said cards
    """
    ret_list = []
    temp_dict = {}
    for deck_list in deck_lists:
        appender = ' (LS)'
        if deck_list[0].startswith('Dark Side'):
            appender = ' (DS)'
        for deck_card, deck_card_qty in deck_list[2].items():
            if deck_card + appender not in temp_dict:
                temp_dict[deck_card + appender] = 0
            temp_dict[deck_card + appender] += deck_card_qty
    for temp_card, temp_card_qty in temp_dict.items():
        ret_list.append((temp_card, temp_card_qty))
    return ret_list

def process_eras(in_era_name, raw_list):
    """
    Process information for the particular format, including decks, the database, suggestions
    """
    return_dict = {}
    format_card_list = []
    format_own = 0
    format_total = 0
    set_index = SETS.index(in_era_name)
    valid_sets = SETS[:set_index+1]
    for in_card in raw_list:
        valid_card = False
        for card_set in in_card[3]:
            if card_set in valid_sets:
                valid_card = True
        if valid_card:
            format_card_list.append(in_card)
            format_total += in_card[6]
            format_own += in_card[5]

    format_cards = len(format_card_list)

    format_decks = read_decks(in_era_name)

    format_decks_minus_own = check_decks(format_decks, format_card_list)
    format_most_needed = aggregate_most_needed(format_decks_minus_own)
    format_most_needed = sorted(format_most_needed, key=lambda x:(-1 * x[1], x[0]))
    format_decks_minus_own = sorted(format_decks_minus_own, key=lambda x:x[1])
    return_dict['FORMAT_OWN'] = format_own
    return_dict['FORMAT_TOTAL'] = format_total
    return_dict['FORMAT_CARDS'] = format_cards
    return_dict['DECKS'] = format_decks_minus_own
    return_dict['NEEDED'] = format_most_needed
    return return_dict

def handle_output(in_era_name, format_dict, dest_fh):
    """
    Handle the output, so I don't have to do this multiple times
    """
    double_print(f"** {in_era_name.upper()} ***", dest_fh)

    tot_str = f"There are {format_dict['FORMAT_CARDS']} {in_era_name} legal cards"
    double_print(tot_str, dest_fh)

    summ_str = f"Have {format_dict['FORMAT_OWN']} out of {format_dict['FORMAT_TOTAL']} - " + \
        f"{100* format_dict['FORMAT_OWN']/format_dict['FORMAT_TOTAL']:.2f} percent of a playset"
    double_print(summ_str, dest_fh)

    ds_done = False
    ls_done = False
    for deck in format_dict['DECKS']:
        if ds_done and ls_done:
            break
        if deck[0].startswith('Dark Side') and not ds_done:
            double_print(f"\nClosest DS deck to completion ({deck[0]}) is at " + \
                f"{deck[1]} cards.", dest_fh)
            double_print(str(deck[2]), dest_fh)
            ds_done = True
        if deck[0].startswith('Light Side') and not ls_done:
            double_print(f"\nClosest LS deck to completion ({deck[0]}) is at " + \
                f"{deck[1]} cards.", dest_fh)
            double_print(str(deck[2]), dest_fh)
            ls_done = True

    print()

in_lines = file_h.readlines()
file_h.close()
in_lines = [line.strip() for line in in_lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
card_lines = []
card_names = set()
duplicate_check = set()
for line in in_lines:
    if line.startswith('//') or line == '':
        continue
    try:
        line = line.split('//')[0].strip()
        card_name, card_side, card_type, card_sets, card_max, card_own = line.split(';')
    except ValueError:
        print("Invalid line:")
        print(line)
        continue
    if card_side not in ['LS', 'DS']:
        print(f"Invalid card side: {card_side}")
    if card_type not in VALID_CARD_TYPES:
        print(line)
        print(f"Unknown card type: {card_type}")
        continue
    card_sets, card_rarities = parse_sets(card_name, card_sets)
    card_names.add(card_name)
    card_max = int(card_max)
    if (card_name, card_side) in duplicate_check:
        print(f"Duplicate: {card_name} - {card_side}")
    duplicate_check.add((card_name, card_side))
    try:
        card_own = int(card_own)
    except ValueError:
        print("Invalid line:")
        print(line)
        continue
    TOTAL_MAX += card_max
    TOTAL_OWN += card_own
    card_lines.append([card_name, card_side, card_type, card_sets, card_rarities,
        card_own, card_max])

side_choice, filtered_list = sort_and_filter(card_lines, 1)
set_choice, filtered_list = sort_and_filter(filtered_list, 3)
type_choice, filtered_list = sort_and_filter(filtered_list, 2)
_, filtered_list = sort_and_filter(filtered_list, 4)
card_name, filtered_list = sort_and_filter(filtered_list, 0)

if __name__=="__main__":
    out_file_h = open(OUT_FILE_NAME, 'w', encoding="UTF-8")

    double_print("Star Wars CCG Inventory Tracker Tool\n", out_file_h)
    double_print(f"There are {len(duplicate_check)} distinct cards in the game.", out_file_h)
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} total cards - " + \
        f"{100 * TOTAL_OWN/TOTAL_MAX:.2f} percent\n", out_file_h)

    SIDE_STR = "Dark Side"
    if side_choice == "LS":
        SIDE_STR = "Light Side"
    double_print(f"Suggested purchase is a {SIDE_STR} {type_choice} from {set_choice}: "\
        f"{card_name} (own {filtered_list[0][5]} out of {filtered_list[0][6]})\n", out_file_h)

    most_needed_total = {}

    # 01 Premiere
    prem_dict = process_eras("Premiere", card_lines)
    for card_tuple in prem_dict['NEEDED']:
        if card_tuple[0] not in most_needed_total:
            most_needed_total[card_tuple[0]] = 0
        most_needed_total[card_tuple[0]] += card_tuple[1]
    handle_output("Premiere", prem_dict, out_file_h)

    # 02 A New Hope
    anh_dict = process_eras("A New Hope", card_lines)
    for card_tuple in anh_dict['NEEDED']:
        if card_tuple[0] not in most_needed_total:
            most_needed_total[card_tuple[0]] = 0
        most_needed_total[card_tuple[0]] += card_tuple[1]
    handle_output("A New Hope", anh_dict, out_file_h)

    # 03 Hoth
    hoth_dict = process_eras("Hoth", card_lines)
    for card_tuple in hoth_dict['NEEDED']:
        if card_tuple[0] not in most_needed_total:
            most_needed_total[card_tuple[0]] = 0
        most_needed_total[card_tuple[0]] += card_tuple[1]
    handle_output("Hoth", hoth_dict, out_file_h)

    # 04 Dagobah
    dago_dict = process_eras("Dagobah", card_lines)
    for card_tuple in dago_dict['NEEDED']:
        if card_tuple[0] not in most_needed_total:
            most_needed_total[card_tuple[0]] = 0
        most_needed_total[card_tuple[0]] += card_tuple[1]
    handle_output("Dagobah", dago_dict, out_file_h)

    # 05 Cloud City
    cc_dict = process_eras("Cloud City", card_lines)
    for card_tuple in cc_dict['NEEDED']:
        if card_tuple[0] not in most_needed_total:
            most_needed_total[card_tuple[0]] = 0
        most_needed_total[card_tuple[0]] += card_tuple[1]
    handle_output("Cloud City", cc_dict, out_file_h)

    # 06 Jabba's Palace
    jabba_dict = process_eras("Jabba's Palace", card_lines)
    for card_tuple in jabba_dict['NEEDED']:
        if card_tuple[0] not in most_needed_total:
            most_needed_total[card_tuple[0]] = 0
        most_needed_total[card_tuple[0]] += card_tuple[1]
    handle_output("Jabba's Palace", jabba_dict, out_file_h)

    most_needed_total = list(most_needed_total.items())
    most_needed_total = sorted(most_needed_total, key=lambda x:(-1 * x[1], x[0]))
    double_print("Most needed cards are:", out_file_h)
    for pr_card_tuple in most_needed_total[:10]:
        double_print(f" - {pr_card_tuple[0]}: {pr_card_tuple[1]}", out_file_h)

    out_file_h.close()
