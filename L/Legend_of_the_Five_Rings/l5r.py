#!/usr/bin/python3

"""
Inventory tracker and purchase selector for the Legend of the Five Rings CCG
"""

import os
import re

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter
from card_games.General.Libraries.check_inventory import check_inventory

GAME_NAME = "Legend of the Five Rings"

FILE_PREFIX = "card_games/L/Legend_of_the_Five_Rings"

if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "L/Legend_of_the_Five_Rings"

with open(FILE_PREFIX + '/Data/L5RData.txt', 'r', encoding="UTF-8") as in_file:
    in_lines = in_file.readlines()
DECK_DIR = FILE_PREFIX + "/Decks"
OUT_FILE_NAME = FILE_PREFIX + "/L5ROut.txt"

with open(FILE_PREFIX + '/Data/L5RNameFixer.txt', 'r', encoding="UTF-8") as name_fixer:
    name_fix_lines = name_fixer.readlines()

DYNASTY_CARD_TYPES = ['Region', 'Event', 'Holding', 'Personality', 'Celestial']
FATE_CARD_TYPES = ['Strategy', 'Spell', 'Item', 'Follower', 'Ancestor', 'Ring']
PREGAME_TYPES = ['Stronghold', 'Sensei', 'Wind']

VALID_CLANS = ['Lion', 'Shadowlands', 'Ratling', 'Scorpion', 'Crab', 'Crane', 'Dragon', 'Mantis',
    'Phoenix', 'Spider', 'Naga', 'Unaligned', 'Unicorn', 'Brotherhood of Shinsei', "Toturi's Army",
    'Ninja', 'Spirit', ]

MODERN_SETS = ['Ivory Edition', 'The Dead of Winter', 'Emperor Edition Demo Decks',
    'Death at Koten', 'Promotional-Celestial', 'Promotional-Samurai', 'Before the Dawn',
    'Battle of Kyuden Tonbo', 'The Harbinger', 'Emperor Edition', 'Forgotten Legacy',
    'Second City', 'Promotional-Ivory', 'Glory of the Empire', 'Stronger Than Steel',
    'Celestial Edition', 'The Truest Test', 'Twenty Festivals', 'The Imperial Gift 3',
    'Samurai Edition', 'Tomorrow', "Khan's Defiance", "Promotional-Twenty Festivals",
    "The Plague War", 'The Currency of War', 'Samurai Edition Banzai', 'War of Honor',
    'The Imperial Gift 2', "Empire at War", "A Matter of Honor", "Honor and Treachery",
    "Embers of War", "Words and Deeds", "The Blackest Storm", "Hidden Forest War",
    "The Heaven's Will", "Path of the Destroyer", "Onyx Edition", "Promotional-Emperor",
    "Celestial Edition 15th Anniversary", "The New Order", "The Coming Storm", "Seeds of Decay",
    "A Line in the Sand", "Gates of Chaos", "Test of the Emerald and Jade Championships",
    "Evil Portents", "Aftermath", "Coils of Madness", "Torn Asunder", "The Shadow's Embrace",
    "Thunderous Acclaim", 'The Imperial Gift 1', 'Siege: Clan War', 'Shattered Empire',
    "Rise of Jigoku", "Road to Ruin", "Rise of Otosan Uchi", "Gathering Storms",
    "Chaos Reigns I", 'Gates of Tengoku', 'Chaos Reigns II', 'Chaos Reigns III',
]
PRE_MODERN_SETS = ['Hidden Emperor 6', 'Diamond Edition', 'Training Grounds', 'Winds of Change',
    'Hidden Emperor 4', "Honor's Veil", 'The Dark Journey Home', '1,000 Years of Darkness',
    'The Fall of Otosan Uchi', 'Forbidden Knowledge', 'Lotus Edition', "Ambition's Debt",
    'Test of Enlightenment', 'A Perfect Cut', 'Rise of the Shogun', 'Scorpion Clan Coup 3',
    'Promotional-Lotus', 'Training Grounds 2', 'Hidden City', 'Heaven & Earth', 'Shadowlands',
    'Gold Edition', 'Jade Edition', 'Pearl Edition', 'Crimson and Jade', 'Time of the Void',
    'Path of Hope', 'Anvil of Despair', "An Oni's Fury", 'Honor Bound', 'Promotional-Gold',
    'Promotional-Diamond', 'Scorpion Clan Coup 1', 'The War of Spirits', 'Dark Allies',
    'Promotional-Imperial', 'Soul of the Empire', 'Promotional-Jade', "Imperial Edition",
    "Hidden Emperor 5", "Fire & Shadow", "Emerald Edition", "Obsidian Edition", "Promotional-CWF",
    "Broken Blades", "Hidden Emperor 1", "Storms Over Matsu Palace", "Scorpion Clan Coup 2",
    "Battle of Beiden Pass", "L5R Experience", "Siege of Sleeping Mountain", 'Hidden Emperor 3',
    "Dawn of the Empire", "Reign of Blood", "Enemy of My Enemy", "Drums of War", "Code of Bushido",
    "Web of Lies", "Wrath of the Emperor", "Hidden Emperor 2", "Top Deck Booster Pack",
    "Crab vs. Lion", "Heroes of Rokugan",
]
VALID_FORMATS = ['Clan Wars (Imperial)', 'Hidden Emperor (Jade)', 'Four Winds (Gold)',
    'Rain of Blood (Diamond)', 'Age of Enlightenment (Lotus)', 'Race for the Throne (Samurai)',
    'Destroyer War (Celestial)', 'Age of Conquest (Emperor)',
    "A Brother's Destiny (Ivory Edition)", "A Brother's Destiny (Twenty Festivals)",
    'War of the Seals (Onyx Edition)', 'Shattered Empire', 'Modern', 'BigDeck', 'Ivory Extended', 
    '20F Extended', 'Jade Extended', 'Jade Open', 'Legacy']

FORMAT_MAP = { # Maps a format name to its deck directory
    'Clan Wars (Imperial)':'01 - Imperial',
    'Hidden Emperor (Jade)':'02 - Jade',
    'Jade Extended':'02.5 - Jade Extended',
    'Jade Open':'02.7 - Jade Open',
    'Four Winds (Gold)':'03 - Gold',
    'Rain of Blood (Diamond)':'04 - Diamond',
    'Age of Enlightenment (Lotus)':'05 - Lotus',
    'Race for the Throne (Samurai)':'06 - Samurai',
    'Destroyer War (Celestial)':'07 - Celestial',
    'Age of Conquest (Emperor)':'08 - Emperor',
    "A Brother's Destiny (Ivory Edition)":'09 - Ivory',
    "A Brother's Destiny (Twenty Festivals)":'10 - Twenty Festivals',
    'War of the Seals (Onyx Edition)':'11 - Onyx Edition',
    'Shattered Empire':'12 - Shattered Empire',
    'Modern':'20 - Modern',
    'BigDeck':'21 - BigDeck',
    'Ivory Extended':'22 - Ivory Extended',
    '20F Extended':'23 - 20F Extended',
}

def parse_sets(this_card_name, set_string):
    """
    Take in a set string, and return a tuple:
    ([sets], [rarites], MODERN_LEGAL (bool))
    """
    set_string = set_string.replace('–', '-')
    ret_sets = []
    ret_rarities = set()
    ret_modern_legal = False
    for set_part in set_string.split('/'):
        match_obj = re.search(r"(.*) \((.*)\)", set_part)
        if match_obj:
            this_set, this_set_rarity = match_obj.groups()
            if this_set in MODERN_SETS:
                ret_modern_legal = True
            elif this_set in PRE_MODERN_SETS:
                pass
            else:
                print(f"For card [{this_card_name}]")
                print(f"Unhandled set for modern check: {this_set}")
            ret_sets.append(this_set)
            ret_rarities.add(this_set_rarity)
        else:
            print("[" + this_card_name + "] Issue with: " + set_part)
    return (ret_sets, list(ret_rarities), ret_modern_legal)

def read_decks(deck_format):
    """
    Takes in a format, and returns a list of Deck dicts
    """
    ret_list = []
    format_deck_dir = DECK_DIR + "/" + FORMAT_MAP[deck_format]
    for deck_clan in os.listdir(format_deck_dir):
        if deck_clan in ['Banned List.txt', 'General.txt']:
            continue
        for deck_filename in os.listdir(format_deck_dir + "/" + deck_clan):
            deck_name = deck_clan + "/" + deck_filename
            with open(format_deck_dir + "/" + deck_name, 'r', encoding="UTF-8") as in_deck:
                deck_lines = in_deck.readlines()
            deck_lines = [line.strip() for line in deck_lines]
            this_deck = {}
            for deck_line in deck_lines:
                if deck_line == '' or deck_line.startswith('#'):
                    continue
                if deck_line.startswith('Proxy Personality'):
                    continue
                if deck_line.startswith('Proxy Follower'):
                    continue
                if deck_line.startswith('Proxy Holding'):
                    continue
                if deck_format in ['BigDeck', 'Modern']:
                    deck_card_qty = 1
                    deck_card_name = deck_line.strip()
                else:
                    try:
                        deck_card_qty = int(deck_line.split(' ')[0])
                    except ValueError:
                        print("Error in deck:")
                        print(format_deck_dir + "/" + deck_name)
                        print(deck_line)
                        continue
                    deck_card_name = ' '.join(deck_line.split(' ')[1:]).strip()
                if deck_card_name not in this_deck:
                    this_deck[deck_card_name] = 0
                this_deck[deck_card_name] += deck_card_qty
            ret_list.append({'name':deck_name, 'list':this_deck})
    return ret_list

def check_decks(list_of_decks, list_of_cards, in_name_fix):
    """
    Given:
    - a list of deck objects, and a list of relevant card tuples
    Return:
    - a list of tuples that are [DECK_NAME], [MISSING_NO], [MISSING_CARDS]
    """

    inventory_dict = {}
    for in_card in list_of_cards:
        inventory_dict[in_card[0]] = in_card[7]
        # Potential card name cleanup
        cleanup_rules = {'ó':'o'}
        clean_name = in_card[0]
        for start_letter, change_letter in cleanup_rules.items():
            clean_name = clean_name.replace(start_letter, change_letter)
        if clean_name in in_name_fix:
            inventory_dict[in_name_fix[clean_name]] = in_card[7]
        else:
            inventory_dict[clean_name] = in_card[7]

    ret_list = check_inventory(list_of_decks, inventory_dict)
    return ret_list

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

def process_formats(in_format_name, raw_list, in_name_fix_all):
    """
    Process information for the particular format, including decks, the database, suggestions
    """
    return_dict = {}
    return_dict['FILTERED'] = {}
    format_card_list = []
    return_dict['FORMAT_OWN'] = 0
    return_dict['FORMAT_TOTAL'] = 0
    for in_card in raw_list:
        if in_format_name == in_card[6]:
            format_card_list.append(in_card)
            return_dict['FORMAT_TOTAL'] += in_card[8]
            return_dict['FORMAT_OWN'] += in_card[7]

    return_dict['FORMAT_CARDS'] = len(format_card_list)

    return_dict['FILTERED']['set'], ft_filtered_list = \
        sort_and_filter(format_card_list, 4, by_len = True)
    return_dict['FILTERED']['deck'], ft_filtered_list = sort_and_filter(ft_filtered_list, 2)
    return_dict['FILTERED']['type'], ft_filtered_list = sort_and_filter(ft_filtered_list, 1)
    if return_dict['FILTERED']['type'] in ['Personality', 'Stronghold']:
        _, ft_filtered_list = sort_and_filter(ft_filtered_list, 3)
    _, ft_filtered_list = sort_and_filter(ft_filtered_list, 5)
    return_dict['FILTERED']['name'], ft_filtered_list = sort_and_filter(ft_filtered_list, 0)
    return_dict['ITEM'] = ft_filtered_list[0]

    format_decks = read_decks(in_format_name)

    in_name_fix_format = {}
    for db_card_line in in_name_fix_all:
        db_card_name, this_format, target_name = db_card_line.split(';')
        if this_format == in_format_name:
            in_name_fix_format[db_card_name] = target_name

    format_decks_minus_own = check_decks(format_decks, format_card_list, in_name_fix_format)
    format_most_needed = aggregate_most_needed(format_decks_minus_own)
    format_most_needed = sorted(format_most_needed, key=lambda x:(-1 * x[1], x[0]))
    format_decks_minus_own = sorted(format_decks_minus_own, key=lambda x:x[1])
    return_dict['DECKS'] = format_decks_minus_own
    return_dict['NEEDED'] = format_most_needed
    return return_dict

def handle_output(in_format_name, format_dict, dest_fh):
    """
    Handle the output, so I don't have to do this multiple times
    """
    double_print(f"\n*** {in_format_name.upper()} ***", dest_fh)

    tot_str = f"There are {format_dict['FORMAT_CARDS']} {in_format_name} legal cards"
    double_print(tot_str, dest_fh)

    summ_str = f"Have {format_dict['FORMAT_OWN']} out of {format_dict['FORMAT_TOTAL']} - " + \
        f"{100* format_dict['FORMAT_OWN']/format_dict['FORMAT_TOTAL']:.2f} percent of a playset"
    double_print(summ_str, dest_fh)

    purch_str = f"Chosen card is a(n) {format_dict['FILTERED']['type']} from " + \
        f"{format_dict['FILTERED']['set']} - {format_dict['FILTERED']['name']}. I own " + \
        f"{format_dict['ITEM'][7]} of {format_dict['ITEM'][8]}"
    double_print(purch_str, dest_fh)

    double_print(f"\nClosest deck to completion ({format_dict['DECKS'][0][0]}) is at " + \
        f"{format_dict['DECKS'][0][1]} cards.", dest_fh)
    double_print(str(format_dict['DECKS'][0][2]), dest_fh)

    double_print("\nMost needed cards are:", dest_fh)
    for pr_card_tuple in format_dict['NEEDED'][:10]:
        double_print(f" - {pr_card_tuple[0]}: {pr_card_tuple[1]}", dest_fh)

in_lines = [line.strip() for line in in_lines]

name_fix_lines = [line.strip() for line in name_fix_lines]

TOTAL_MAX = 0
TOTAL_OWN = 0
card_lines = []
card_names = set()
duplicate_check = set()
modern_cards = {} # A dictionary of names -> card lines for Modern legal cards
bigdeck_cards = {} # A dictionary of names -> card lines for Big Deck cards
format_map = {} # For a format summary at the end, given that this is our first criteria
for set_format in VALID_FORMATS:
    format_map[set_format] = [0, 0]
for line in in_lines:
    if line.startswith('#') or line == '':
        continue
    try:
        line = line.split('#')[0].strip()
        card_name, card_type, card_clan, card_sets, card_format, card_max, \
            card_own = line.split(';')
    except ValueError:
        print("Invalid line:")
        print(line)
        continue
    CARD_DECK = ''
    card_type = card_type.split('/')[0]
    if card_type in DYNASTY_CARD_TYPES:
        CARD_DECK = 'Dynasty'
    elif card_type in FATE_CARD_TYPES:
        CARD_DECK = 'Fate'
    elif card_type in PREGAME_TYPES:
        CARD_DECK = 'Pre-Game'
    else:
        print(line)
        print(f"Unknown card type: {card_type}")
        continue
    this_card_clans = []
    for check_clan in card_clan.split('/'):
        if check_clan != '' and check_clan not in VALID_CLANS:
            print(f"Invalid clan: {check_clan}")
            continue
        this_card_clans.append(check_clan)
    card_sets, card_rarities, modern_legal = parse_sets(card_name, card_sets)
    if card_format not in VALID_FORMATS:
        print(f"Invalid format: {card_format}")
        continue
    card_names.add(card_name)
    card_max = int(card_max)
    if (card_name, card_format) in duplicate_check:
        print(f"Duplicate: {card_name} - {card_format}")
    duplicate_check.add((card_name, card_format))
    try:
        card_own = int(card_own)
    except ValueError:
        print("Invalid line:")
        print(line)
        continue
    format_map[card_format][0] += card_own
    format_map[card_format][1] += card_max
    TOTAL_MAX += card_max
    TOTAL_OWN += card_own
    if modern_legal:
        if card_name not in modern_cards:
            modern_cards[card_name] = [card_name, card_type, CARD_DECK, this_card_clans,
                card_sets, card_rarities, 'Modern', min(card_own, 1), 1]
        else:
            modern_cards[card_name][4] = list(set(modern_cards[card_name][4] + card_sets))
            modern_cards[card_name][5] = list(set(modern_cards[card_name][5] + card_rarities))
            modern_cards[card_name][7] = min(modern_cards[card_name][8], \
                modern_cards[card_name][7] + card_own)

    if card_name not in bigdeck_cards:
        bigdeck_cards[card_name] = [[card_name, card_type, CARD_DECK, this_card_clans, card_sets,
            card_rarities, card_format, card_own, card_max]]
    else:
        bigdeck_cards[card_name].append([card_name, card_type, CARD_DECK, this_card_clans,
            card_sets, card_rarities, card_format, card_own, card_max])

    card_lines.append([card_name, card_type, CARD_DECK, this_card_clans, card_sets, card_rarities,
        card_format, card_own, card_max])

for _, card_item in modern_cards.items():
    card_lines.append(card_item)
    format_map['Modern'][0] += card_item[7]
    format_map['Modern'][1] += card_item[8]

# Do work for Jade Extended
jade_extended_cards = []
imp_holding = []
jade_names = set()
for card in card_lines:
    if card[6] == 'Hidden Emperor (Jade)':
        jade_extended_cards.append(card)
        jade_names.add(card[0])
    if card[6] == 'Clan Wars (Imperial)':
        if card[1] in ['Holding', 'Region', 'Follower', 'Ancestor', 'Item', 'Strategy']:
            imp_holding.append(card)
for card in jade_extended_cards:
    new_card = card.copy()
    new_card[6] = 'Jade Extended'
    card_lines.append(new_card)
    format_map['Jade Extended'][0] += new_card[7]
    format_map['Jade Extended'][1] += new_card[8]
for card in imp_holding:
    if card[0] not in jade_names:
        new_card = card.copy()
        new_card[6] = 'Jade Extended'
        card_lines.append(new_card)
        format_map['Jade Extended'][0] += new_card[7]
        format_map['Jade Extended'][1] += new_card[8]

# Do work for Jade Open
jade_open_cards = []
imp_holding = []
jade_names = set()
for card in card_lines:
    if card[6] == 'Hidden Emperor (Jade)':
        jade_open_cards.append(card)
        jade_names.add(card[0])
    if card[6] == 'Clan Wars (Imperial)':
        imp_holding.append(card)
for card in jade_open_cards:
    new_card = card.copy()
    new_card[6] = 'Jade Open'
    card_lines.append(new_card)
    format_map['Jade Open'][0] += new_card[7]
    format_map['Jade Open'][1] += new_card[8]
for card in imp_holding:
    if card[0] not in jade_names:
        new_card = card.copy()
        new_card[6] = 'Jade Open'
        card_lines.append(new_card)
        format_map['Jade Open'][0] += new_card[7]
        format_map['Jade Open'][1] += new_card[8]

# Get things set up for Big Deck
for card_name, card_printings in bigdeck_cards.items():
    most_recent_card = card_printings[0].copy()
    if len(card_printings) == 1 and most_recent_card[6] == 'BigDeck':
        continue
    for card_printing in card_printings:
        if VALID_FORMATS.index(card_printing[6]) > VALID_FORMATS.index(most_recent_card[6]):
            most_recent_card = card_printing.copy()
    most_recent_card[6] = 'BigDeck'
    most_recent_card[7] = min(1, most_recent_card[7])
    most_recent_card[8] = 1
    card_lines.append(most_recent_card)
    format_map['BigDeck'][0] += most_recent_card[7]
    format_map['BigDeck'][1] += most_recent_card[8]

# Get cards into position to check for Extended arcs
ivory_extended_cards = {}
twenty_f_extended_cards = {}
for card in card_lines:
    if card[6] in ["A Brother's Destiny (Ivory Edition)", "A Brother's Destiny (Twenty Festivals)"]:
        if card[0] not in ivory_extended_cards:
            ivory_extended_cards[card[0]] = []
        if card[0] not in twenty_f_extended_cards:
            twenty_f_extended_cards[card[0]] = []
        ivory_extended_cards[card[0]].append(card.copy())
        twenty_f_extended_cards[card[0]].append(card.copy())
    if card[6] == "Age of Conquest (Emperor)":
        if card[0] not in ivory_extended_cards:
            ivory_extended_cards[card[0]] = []
        ivory_extended_cards[card[0]].append(card.copy())
    if card[6] == "War of the Seals (Onyx Edition)":
        if card[0] not in twenty_f_extended_cards:
            twenty_f_extended_cards[card[0]] = []
        twenty_f_extended_cards[card[0]].append(card.copy())

# Get things set up for Ivory Extended (Emperor, Ivory, 20F)
for card_name, card_printings in ivory_extended_cards.items():
    if len(card_printings) == 1:
        this_printing = card_printings[0]
        this_printing[6] = 'Ivory Extended'
        card_lines.append(this_printing.copy())
        format_map['Ivory Extended'][0] += this_printing[7]
        format_map['Ivory Extended'][1] += this_printing[8]
    else:
        this_printing = card_printings[0]
        for card_printing in card_printings:
            if VALID_FORMATS.index(card_printing[6]) > VALID_FORMATS.index(this_printing[6]):
                this_printing = card_printing
        this_printing[6] = 'Ivory Extended'
        card_lines.append(this_printing.copy())
        format_map['Ivory Extended'][0] += this_printing[7]
        format_map['Ivory Extended'][1] += this_printing[8]

# Get things set up for 20F Extended (Ivory, 20F, Onyx)
for card_name, card_printings in twenty_f_extended_cards.items():
    if len(card_printings) == 1:
        this_printing = card_printings[0]
        this_printing[6] = '20F Extended'
        card_lines.append(this_printing.copy())
        format_map['20F Extended'][0] += this_printing[7]
        format_map['20F Extended'][1] += this_printing[8]
    else:
        this_printing = card_printings[0]
        for card_printing in card_printings:
            if VALID_FORMATS.index(card_printing[6]) > VALID_FORMATS.index(this_printing[6]):
                this_printing = card_printing
        this_printing[6] = '20F Extended'
        card_lines.append(this_printing.copy())
        format_map['20F Extended'][0] += this_printing[7]
        format_map['20F Extended'][1] += this_printing[8]

format_choice, filtered_list = sort_and_filter(card_lines, 6)
deck_choice, filtered_list = sort_and_filter(filtered_list, 2)
set_choice, filtered_list = sort_and_filter(filtered_list, 4)
type_choice, filtered_list = sort_and_filter(filtered_list, 1)
CLAN_CHOICE = ""
if type_choice in ['Personality', 'Stronghold']:
    CLAN_CHOICE, filtered_list = sort_and_filter(filtered_list, 3)
_, filtered_list = sort_and_filter(filtered_list, 5)
card_name, filtered_list = sort_and_filter(filtered_list, 0)

if __name__=="__main__":
    out_file_h = open(OUT_FILE_NAME, 'w', encoding="UTF-8")

    double_print("Legend of the Five Rings CCG Inventory Tracker Tool\n", out_file_h)
    double_print(f"There are {len(card_names)} distinct cards in the game.", out_file_h)
    double_print(f"I own {TOTAL_OWN} out of {TOTAL_MAX} total cards - " + \
        f"{100 * TOTAL_OWN/TOTAL_MAX:.2f} percent\n", out_file_h)

    if CLAN_CHOICE == "":
        type_str = type_choice
    else:
        type_str = CLAN_CHOICE + " " + type_choice
    double_print(f"Suggested purchase is a {type_str} from {set_choice}: {card_name} (own " + \
        f"{filtered_list[0][7]} out of {filtered_list[0][8]})", out_file_h)

    # 01 Imperial
    imperial_dict = process_formats("Clan Wars (Imperial)", card_lines, name_fix_lines)
    handle_output("Clan Wars (Imperial)", imperial_dict, out_file_h)

    # 02 Jade
    jade_dict = process_formats("Hidden Emperor (Jade)", card_lines, name_fix_lines)
    handle_output("Hidden Emperor (Jade)", jade_dict, out_file_h)

    # 02.5 Jade Extended
    jadeX_dict = process_formats("Jade Extended", card_lines, name_fix_lines)
    handle_output("Jade Extended", jadeX_dict, out_file_h)

    # 02.7 Jade Open
    jadeopen_dict = process_formats("Jade Open", card_lines, name_fix_lines)
    handle_output("Jade Open", jadeopen_dict, out_file_h)

    # 03 Gold
    gold_dict = process_formats("Four Winds (Gold)", card_lines, name_fix_lines)
    handle_output("Four Winds (Gold)", gold_dict, out_file_h)

    # 04 Diamond
    diamond_dict = process_formats("Rain of Blood (Diamond)", card_lines, name_fix_lines)
    handle_output("Rain of Blood (Diamond)", diamond_dict, out_file_h)

    # 05 Lotus Arc
    lotus_dict = process_formats("Age of Enlightenment (Lotus)", card_lines, name_fix_lines)
    handle_output("Age of Enlightenment (Lotus)", lotus_dict, out_file_h)

    # 06 Samurai Arc
    samurai_dict = process_formats("Race for the Throne (Samurai)", card_lines, name_fix_lines)
    handle_output("Race for the Throne (Samurai)", samurai_dict, out_file_h)

    # 07 Celestial Arc
    celestial_dict = process_formats("Destroyer War (Celestial)", card_lines, name_fix_lines)
    handle_output("Destroyer War (Celestial)", celestial_dict, out_file_h)

    # 08 Emperor Arc
    emperor_dict = process_formats("Age of Conquest (Emperor)", card_lines, name_fix_lines)
    handle_output("Age of Conquest (Emperor)", emperor_dict, out_file_h)

    # 09 Ivory Arc
    ivory_dict = process_formats("A Brother's Destiny (Ivory Edition)", card_lines, name_fix_lines)
    handle_output("A Brother's Destiny (Ivory Edition)", ivory_dict, out_file_h)

    # 10 Twenty Festivals
    twentyF_dict = process_formats("A Brother's Destiny (Twenty Festivals)", card_lines,
        name_fix_lines)
    handle_output("A Brother's Destiny (Twenty Festivals)", twentyF_dict, out_file_h)

    # 11 Onyx Edition
    onyx_dict = process_formats("War of the Seals (Onyx Edition)", card_lines, name_fix_lines)
    handle_output("War of the Seals (Onyx Edition)", onyx_dict, out_file_h)

    # 12 Shattered Empire
    shattered_dict = process_formats("Shattered Empire", card_lines, name_fix_lines)
    handle_output("Shattered Empire", shattered_dict, out_file_h)

    # 20 Modern
    modern_dict = process_formats("Modern", card_lines, name_fix_lines)
    handle_output("Modern", modern_dict, out_file_h)

    # 21 Big Deck
    big_dict = process_formats("BigDeck", card_lines, name_fix_lines)
    handle_output("BigDeck", big_dict, out_file_h)

    double_print("\nCurrent inventory percentage by format:", out_file_h)
    format_sorter = format_map.items()
    format_sorter = sorted(format_sorter, key=lambda x:(-1 * x[1][0]/x[1][1], x[1][1] - x[1][0]))
    for format_name, fown in format_sorter:
        double_print(f"{format_name}: {100*fown[0]/fown[1]:.2f} ({fown[0]}/{fown[1]})", out_file_h)

    out_file_h.close()
