#!/usr/bin/python

"""
Collection tracker/management for Magic: The Gathering
"""

import datetime
import os
import re

from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter
from card_games.M.Magic_the_Gathering.Libraries import mtg_sets

GAME_NAME = "Magic: The Gathering"

FILE_PREFIX = "card_games/M/Magic_the_Gathering"

file_h = open(FILE_PREFIX + '/Data/MTGCardData.txt', 'r', encoding="UTF-8")
restr_file_h = open(FILE_PREFIX + '/Data/MTGRestrictions.txt', 'r', encoding="UTF-8")
commander_cat_fh = open(FILE_PREFIX + '/Data/MTGCommanderCategories.txt', 'r', encoding="UTF-8")
card_corrections_fh = open(FILE_PREFIX + '/Data/MTG Card Corrections.txt', 'r', encoding="UTF-8")
DECK_DIR = FILE_PREFIX + "/Decks"

raw_list = [] # Will hold the full list of cards

class Deck:
    """
    Helper class for a deck, keeping a track of the name and composition
    """
    def __init__(self, deck_name, deck_cards, deck_date=None):
        """
        Basic constructor
        """
        self.deck_name = deck_name
        self.deck_cards = deck_cards
        self.deck_date = deck_date
    def __str__(self):
        """
        String representation
        """
        return f"Deck Name: {self.deck_name} - {self.deck_cards}"
    def __eq__(self, value) -> bool:
        """
        Determines if two decks match
        """
        return self.deck_cards == value.deck_cards

def fix_card_name(in_card_name, correction_dict):
    """
    Handle various ways that cards are written different than the Oracle official way
    """
    if in_card_name in correction_dict:
        return correction_dict[in_card_name]
    return in_card_name

def read_decks(deck_format, correction_dict):
    """
    Takes in a format, and returns a list of Deck objects
    """
    ret_list = []
    deck_format = deck_format.replace("'s", "")
    if deck_format in ['Commander', 'Oathbreaker']:
        for comm_color in os.listdir(DECK_DIR + '/' + deck_format):
            for deck_file in os.listdir(DECK_DIR + '/' + deck_format + "/" + comm_color):
                deck_date = None
                deck_name = deck_file.replace('.txt', '')
                this_deck = {}
                deck_filename = DECK_DIR + '/' + deck_format + '/' + comm_color + "/" + deck_file
                with open(deck_filename, 'r', encoding='UTF-8') as deck_fh:
                    deck_lines = deck_fh.readlines()
                deck_lines = [line.strip() for line in deck_lines]
                for deck_line in deck_lines:
                    if deck_line == '':
                        continue
                    if deck_line.startswith('//') :
                        date_str = deck_line.split(' ')[2]
                        try:
                            deck_date = datetime.datetime.strptime(date_str, "%m/%d/%y")
                        except ValueError:
                            print(f"Invalid date found in {comm_color + '/' + deck_file}")
                            print(f"Invalid date of [{date_str}]")
                            raise
                        continue
                    deck_card_qty = int(deck_line.split(' ')[0])
                    deck_card_name = ' '.join(deck_line.split(' ')[1:]).strip()
                    deck_card_name = fix_card_name(deck_card_name, correction_dict)
                    if deck_card_name not in this_deck:
                        this_deck[deck_card_name] = 0
                    this_deck[deck_card_name] += deck_card_qty
                if deck_date is None:
                    print(f"Invalid date found in {comm_color + '/' + deck_file}")
                    raise ValueError
                ret_list.append(Deck(comm_color + "/" + deck_name, this_deck, deck_date))
    elif deck_format in os.listdir(DECK_DIR):
        for deck_file in os.listdir(DECK_DIR + '/' + deck_format):
            deck_name = deck_file.replace('.txt', '')
            this_deck = {}
            deck_filename = DECK_DIR + '/' + deck_format + '/' + deck_file
            with open(deck_filename, 'r', encoding='UTF-8') as deck_fh:
                deck_lines = deck_fh.readlines()
            deck_lines = [line.strip() for line in deck_lines]
            for deck_line in deck_lines:
                if deck_line.startswith('//') or deck_line == '':
                    continue
                deck_card_qty = int(deck_line.split(' ')[0])
                deck_card_name = ' '.join(deck_line.split(' ')[1:])
                deck_card_name = fix_card_name(deck_card_name, correction_dict)
                if deck_card_name not in this_deck:
                    this_deck[deck_card_name] = 0
                this_deck[deck_card_name] += deck_card_qty
            ret_list.append(Deck(deck_name, this_deck))
    return ret_list

def check_decks(list_of_decks, list_of_cards):
    """
    Given:
    - a list of deck objects, and a list of relevant card tuples
    Return:
    - a list of tuples that are [DECK_NAME], [MISSING_NO], [MISSING_CARDS]
    """
    ret_list = []
    # First, construct a dict of the cards in the format
    inventory_dict = {}
    for in_card in list_of_cards:
        inventory_dict[in_card[0]] = in_card[7]
        #Potential card name cleanup
        cleanup_rules = {'û':'u', 'ó':'o'}
        clean_name = in_card[0]
        for start_letter, change_letter in cleanup_rules.items():
            clean_name = clean_name.replace(start_letter, change_letter)
        inventory_dict[clean_name] = in_card[7]
    for c_deck in list_of_decks:
        this_deck_missing = 0
        this_deck_missing_cards = {}
        for this_card, card_count in c_deck.deck_cards.items():
            if this_card in inventory_dict:
                if card_count > inventory_dict[this_card]:
                    this_deck_missing += card_count - inventory_dict[this_card]
                    this_deck_missing_cards[this_card] = card_count - inventory_dict[this_card]
            else:
                print(f"Missing card {this_card}")
                this_deck_missing += card_count
                this_deck_missing_cards[this_card] = card_count
        ret_list.append((c_deck.deck_name, this_deck_missing, this_deck_missing_cards))
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

def parse_restrictions(restr_lines):
    """
    Create a list of restrictions for each card, if relevant
    """
    return_dict = {}
    for rest_line in restr_lines:
        this_card_name, card_restrictions = rest_line.strip().split(';')
        return_dict[this_card_name] = {}
        for restriction in card_restrictions.split('/'):
            if restriction == 'Relentless':
                return_dict[this_card_name]['All'] = 'Relentless'
            else:
                this_format, bnr = restriction.split('-')
                if this_format not in ['Legacy', 'Vintage', 'Commander', 'Pauper', 'Modern',
                        'Standard', 'Pioneer', 'Oathbreaker', 'Ice Age Block', 'Mirage Block',
                        'Tempest Block', "Urza's Block", "Pauper Commander", "Masques Block",
                        'Invasion Block', 'Odyssey Block', 'Onslaught Block', 'Mirrodin Block',
                        'Kamigawa Block', 'Ravnica Block', 'Premodern']:
                    print("Unknown format: " + this_format)
                if bnr not in ['Banned', 'Restricted']:
                    print("Unknown status: " + bnr)
                return_dict[this_card_name][this_format] = bnr
    return return_dict

    # Dominaria block (Dominaria United/The Brothers' War)
    # Innistrad block (Innistrad: Midnight Hunt/Innistrad: Crimson Vow)
    # Guilds of Ravnica block. ( Guilds of Ravnica, Ravnica Allegiance, War of the Spark)
    # Ixalan block (Ixalan, Rivals of Ixalan)
    # Amonkhet block (Amonkhet, Hour of Devastation)
    # Kaladesh block (Kaladesh, Aether Revolt)
    # Shadows over Innistrad block (Shadows over Innistrad, Eldritch Moon)
    # Battle for Zendikar block (Battle for Zendikar, Oath of the Gatewatch)
    # Khans of Tarkir block (Khans of Tarkir, Fate Reforged, Dragons of Tarkir)
    # Theros block (Theros, Born of the Gods, Journey into Nyx)
    # Return to Ravnica block (Return to Ravnica, Gatecrash, Dragon's Maze)
    # Innistrad block (Innistrad, Dark Ascension, Avacyn Restored)
    # Scars of Mirrodin block (Scars of Mirrodin, Mirrodin Besieged, New Phyrexia)
    # Zendikar block (Zendikar, Worldwake, Rise of the Eldrazi)
    # Alara block (Shards of Alara, Conflux, Alara Reborn)
    # Lorwyn–Shadowmoor block (Lorwyn, Morningtide, Shadowmoor, Eventide)
    # Time Spiral block (Time Spiral, Planar Chaos, Future Sight)

def parse_sets(this_card_name, card_set_string, card_restrictions):
    """
    The heavy lifting function of this module, where I go through and figure out rarites, sets,
    formats, and anything else
    """
    ret_sets = []
    ret_rarities = set()
    ret_formats = {"Commander": 1, "Vintage": 4, "Legacy": 4, "Oathbreaker":1}
    this_card_max = 1
    for card_set in card_set_string.split('/'):
        match_obj = re.search(r"(.*) \((.*)\)", card_set)
        if match_obj:
            this_set, this_set_rarity = match_obj.groups()
            if this_set in mtg_sets.LEGACY_SETS:
                ret_sets.append(this_set)
                ret_rarities.add(this_set_rarity)
            elif this_set in mtg_sets.ARENA_SETS or this_set in mtg_sets.NON_SETS:
                pass # We don't care one bit about Arena sets
            elif this_set in mtg_sets.MTGO_SETS:
                # We don't track the set, but the rarity matters
                ret_rarities.add(this_set_rarity)
            elif this_set in mtg_sets.STANDARD_SETS:
                ret_sets.append(this_set)
                ret_rarities.add(this_set_rarity)
                ret_formats['Standard'] = 4
                ret_formats['Pioneer'] = 4
                ret_formats['Modern'] = 4
            elif this_set in mtg_sets.PIONEER_SETS:
                ret_sets.append(this_set)
                ret_rarities.add(this_set_rarity)
                ret_formats['Pioneer'] = 4
                ret_formats['Modern'] = 4
            elif this_set in mtg_sets.MODERN_SETS:
                ret_sets.append(this_set)
                ret_rarities.add(this_set_rarity)
                ret_formats['Modern'] = 4
            else:
                print("[" + this_card_name + "] Handle: " + this_set)
            if this_set in mtg_sets.PREMODERN_SETS:
                ret_sets.append(this_set)
                ret_rarities.add(this_set_rarity)
                ret_formats['Premodern'] = 4
            # Handle Ice Age Block
            if this_set in ['Ice Age', 'Coldsnap', 'Alliances']:
                ret_formats['Ice Age Block'] = 4
            # Handle Mirage Block
            if this_set in ['Mirage', 'Visions', 'Weatherlight']:
                ret_formats['Mirage Block'] = 4
            # Handle Tempest Block
            if this_set in ['Tempest', 'Stronghold', 'Exodus']:
                ret_formats['Tempest Block'] = 4
            # Handle Urza's Block
            if this_set in ["Urza's Saga", "Urza's Legacy", "Urza's Destiny"]:
                ret_formats["Urza's Block"] = 4
            # Handles Masques Block
            if this_set in ['Mercadian Masques', 'Nemesis', 'Prophecy']:
                ret_formats['Masques Block'] = 4
            # Handles Invasion Block
            if this_set in ['Invasion', 'Planeshift', 'Apocalypse']:
                ret_formats['Invasion Block'] = 4
            # Handles Odyssey block (Odyssey, Torment, Judgment)
            if this_set in ['Odyssey', 'Torment', 'Judgment']:
                ret_formats['Odyssey Block'] = 4
            # Handles Onslaught block (Onslaught, Legions, Scourge)
            if this_set in ['Onslaught', 'Legions', 'Scourge']:
                ret_formats['Onslaught Block'] = 4
            # Handles Mirrodin block (Mirrodin, Darksteel, Fifth Dawn)
            if this_set in ['Mirrodin', 'Darksteel', 'Fifth Dawn']:
                ret_formats['Mirrodin Block'] = 4
            # Handles Kamigawa block (Champions/Betrayers/Saviors of Kamigawa)
            if this_set in ['Champions of Kamigawa', 'Betrayers of Kamigawa', \
                'Saviors of Kamigawa']:
                ret_formats['Kamigawa Block'] = 4
            # Ravnica block (Ravnica: City of Guilds, Guildpact, Dissension)
            if this_set in ['Ravnica: City of Guilds', 'Guildpact', 'Dissension']:
                ret_formats['Ravnica Block'] = 4
        else:
            print("[" + this_card_name + "] Issue with: " + card_set)
    if 'Common' in ret_rarities or 'Land' in ret_rarities:
        ret_formats['Pauper'] = 4
        ret_formats['Pauper Commander'] = 1
    is_relentless = False
    if card_restrictions:
        for restriction_format, restriction_bnr in card_restrictions.items():
            if restriction_bnr == 'Banned':
                del ret_formats[restriction_format]
            elif restriction_bnr == 'Restricted':
                ret_formats[restriction_format] = 1
            elif restriction_bnr == 'Relentless':
                is_relentless = True
            else:
                print(restriction_format)
                print(restriction_bnr)
    if len(ret_formats) == 0:
        ret_formats = {"Vintage": 1}
    if is_relentless:
        for format_name in ret_formats:
            ret_formats[format_name] = 25
    for format_name, format_qty in ret_formats.items():
        this_card_max = max(this_card_max, format_qty)
    ret_rarities = list(ret_rarities)
    return(ret_sets, ret_rarities, ret_formats, this_card_max)

def get_categories(in_lines):
    """
    Return a mapping of Universe Beyond Types to valid Commmanders
    """
    ret_dict = {}
    for cat_line in in_lines:
        cat_line = cat_line.strip()
        cmdr, category = cat_line.split(';')
        if category in ['Fallout', ]:
            category = 'Other'
        if category not in ret_dict:
            ret_dict[category] = []
        ret_dict[category].append(cmdr)
    return ret_dict

def get_corrections(in_lines):
    """
    Create a card correction dict from the data in in_lines
    """
    ret_dict = {}
    for data_line in in_lines:
        data_line = data_line.strip()
        start_card, end_card = data_line.split(';')
        ret_dict[start_card] = end_card
    return ret_dict

def validate_colors(in_colors):
    """
    Takes in a string of colors, and returns a list with the full color names
    """
    ret_colors = []
    color_map = {'C':'Colorless', 'B':'Black', 'U':'Blue', 'R':'Red', 'W':'White',
        'G':'Green'}
    for color in in_colors.split('/'):
        if color not in color_map:
            print("Invalid color: " + color)
        else:
            ret_colors.append(color_map[color])
    return ret_colors

def validate_types(card_type_string):
    """
    Take a string of card types, and return both the card type(s) and subtype(s)
    """
    ret_type = []
    ret_subtype = []
    if '-' in card_type_string:
        types, subtypes = card_type_string.split(' - ')
        types = types.strip()
        subtypes = subtypes.strip()
    else:
        types = card_type_string
        subtypes = ''
    if types == 'Basic Land' or types in 'World Enchantment':
        ret_type.append(types)
        types = ''
    if types == 'Basic Snow Land':
        ret_type.append('Basic Land')
        ret_type.append('Snow')
        types = ''
    for check_type in types.split(' '):
        if check_type == '':
            continue
        if check_type in ['Artifact', 'Creature', 'Enchantment', 'Sorcery', "Instant",
                "Legendary", 'Land', 'Planeswalker', 'Vanguard', 'Kindred', 'Scheme',
                'Snow',]:
            ret_type.append(check_type)
        else:
            print("Unknown type: " + check_type)
    for check_type in subtypes.split(' '):
        if check_type != '':
            ret_subtype.append(check_type)
    return(ret_type, ret_subtype)

def process_formats(format_name, correction_dict):
    """
    Given a format_name, process everything we need- find the suggested card, give stats on 
    the format, and parse, and sort the various decks.
    """
    return_dict = {}
    return_dict['FILTERED'] = {}
    format_card_list = []
    format_own = 0
    format_total = 0
    for in_card in raw_list:
        if format_name in in_card[6]:
            format_card_list.append(in_card)
            format_total += in_card[6][format_name]
            format_own += min(in_card[7], in_card[6][format_name])
    format_cards = len(format_card_list)
    FORMAT_LIST.append((format_name, format_own, format_total))

    return_dict['FILTERED']['set'], ft_filtered_list = \
        sort_and_filter(format_card_list, 4, by_len = True)
    return_dict['FILTERED']['type'], ft_filtered_list = sort_and_filter(ft_filtered_list, 1)
    if return_dict['FILTERED']['type'] in ['Creature', 'Planeswalker']:
        _, ft_filtered_list = sort_and_filter(ft_filtered_list, 2)
    _, ft_filtered_list = sort_and_filter(ft_filtered_list, 3)
    _, ft_filtered_list = sort_and_filter(ft_filtered_list, 5)
    return_dict['FILTERED']['name'], ft_filtered_list = sort_and_filter(ft_filtered_list, 0)
    return_dict['ITEM'] = ft_filtered_list[0]

    format_decks = read_decks(format_name, correction_dict)
    oldest_deck = (datetime.datetime.today(), '')
    if format_name in ["Commander", "Oathbreaker"]:
        for this_deck in format_decks:
            if this_deck.deck_date < oldest_deck[0]:
                oldest_deck = (this_deck.deck_date, this_deck.deck_name)

    format_decks_minus_own = check_decks(format_decks, format_card_list)
    format_most_needed = aggregate_most_needed(format_decks_minus_own)
    format_most_needed = sorted(format_most_needed, key=lambda x:(-1 * x[1], x[0]))
    format_decks_minus_own = sorted(format_decks_minus_own, key=lambda x:x[1])
    return_dict['FORMAT_OWN'] = format_own
    return_dict['FORMAT_TOTAL'] = format_total
    return_dict['FORMAT_CARDS'] = format_cards
    return_dict['DECKS'] = format_decks_minus_own
    return_dict['NEEDED'] = format_most_needed
    return_dict['OLDEST'] = oldest_deck
    return return_dict

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
        f"{format_dict['ITEM'][7]} of {format_dict['ITEM'][6][format_name]}"
    double_print(purch_str, dest_fh)

    if format_name != 'Commander':
        double_print(f"\nClosest deck to completion ({format_dict['DECKS'][0][0]}) is at " + \
            f"{format_dict['DECKS'][0][1]} cards.", dest_fh)
        double_print(str(format_dict['DECKS'][0][2]), dest_fh)

    double_print("\nMost needed cards are:", dest_fh)
    for pr_card_tuple in format_dict['NEEDED'][:10]:
        double_print(f" - {pr_card_tuple[0]}: {pr_card_tuple[1]}", dest_fh)

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

restrictions = parse_restrictions(restr_file_h.readlines())
restr_file_h.close()

commander_cats = get_categories(commander_cat_fh.readlines())
commander_cat_fh.close()

card_corrections = get_corrections(card_corrections_fh.readlines())

SET_CHECK = 0
CHECK_SET = "Champions of Kamigawa"
CHECK_AMOUNT = 306
SET_CHECK += 15 # Extra basic lands

TOTAL_OWN = 0
TOTAL_MAX = 0
card_names = set()
creature_types = {}
PLANESWALKER_COUNT = 0
planeswalkers = {}
FIRST_MANA_NEEDED_CARD = ''
MANA_CARDS_DONE = 0

for line in lines:
    if line == '' or line.startswith('#'):
        continue
    if line.count(';') == 4:
        try:
            card_name, card_type, card_colors, card_sets, card_qty = line.split(';')
            CARD_MANA_VALUE = 'X'
            if FIRST_MANA_NEEDED_CARD == '':
                FIRST_MANA_NEEDED_CARD = card_name
        except ValueError:
            print("Error in line:")
            print(line)
            continue
    else:
        try:
            card_name, card_type, card_colors, CARD_MANA_VALUE, card_sets, card_qty = \
                line.split(';')
        except ValueError:
            print("Error in line:")
            print(line)
            continue
    if card_name in card_names:
        print(f"Duplicate: {card_name}")
    card_names.add(card_name)
    if CARD_MANA_VALUE != '' and CARD_MANA_VALUE != "X":
        try:
            CARD_MANA_VALUE = int(CARD_MANA_VALUE)
            MANA_CARDS_DONE += 1
        except ValueError:
            print("Something wrong with line:")
            print(line)
            continue
    try:
        card_qty = int(card_qty)
    except ValueError:
        print("Something wrong with line:")
        print(line)
        continue
    card_colors = validate_colors(card_colors)
    card_type = card_type.replace('—', '-')
    card_type = card_type.replace('\u2013', '-')
    card_type, card_subtype = validate_types(card_type)

    if 'Creature' in card_type:
        for subtype in card_subtype:
            if subtype not in creature_types:
                creature_types[subtype] = 0
            creature_types[subtype] += 1

    if 'Planeswalker' in card_type:
        for subtype in card_subtype:
            if subtype not in planeswalkers:
                planeswalkers[subtype] = []
            planeswalkers[subtype].append(card_name)
            PLANESWALKER_COUNT += 1

    card_sets, card_rarities, card_formats, CARD_MAX = parse_sets(card_name, card_sets, \
        restrictions.get(card_name))
    if CHECK_SET in card_sets:
    #if CHECK_SET in card_sets and 'Blue' in card_colors:
    #if CHECK_SET in card_sets and 'Green' in card_colors and 'Creature' not in card_type:
    #if CHECK_SET in card_sets and 'Artifact' in card_type:
        #print(card_name)
        SET_CHECK += 1
    if 'Basic Land' in card_type:
        for card_format in card_formats:
            if card_format == 'Commander':
                card_formats[card_format] = 40
            else:
                card_formats[card_format] = 30
        CARD_MAX = 40
    if 'Scheme' in card_type:
        card_formats = {'Vintage':1}
        CARD_MAX = 1
    if 'Vanguard' in card_type:
        card_formats = {'Vintage':1}
        card_sets = ['Vanguard']
        card_rarites = ['Special']
        CARD_MAX = 1
    if 'Creature' in card_type and 'Uncommon' in card_rarities:
        card_formats['Pauper Commander'] = 1
    TOTAL_MAX += CARD_MAX
    TOTAL_OWN += card_qty
    raw_list.append((card_name, card_type, card_subtype, card_colors, card_sets, card_rarities, \
        card_formats, card_qty, CARD_MAX))

FORMAT_LIST = []

PLAYABLE_CARDS = 0
for card in raw_list:
    VALID_CARD = True
    if 'Scheme' in card[1] or 'Vanguard' in card[1]:
        VALID_CARD = False
    if VALID_CARD:
        PLAYABLE_CARDS += 1
    if 'Vintage' not in card[6]:
        if 'Premodern' not in card[6]:
            print("No Vintage?")
            print(card)

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/MTGOut.txt", 'w', encoding="UTF-8")

    double_print("Magic: The Gathering Collection Tracker\n", out_file_h)

    double_print(f"Tracking {len(raw_list)} items ({PLAYABLE_CARDS} actual cards).", out_file_h)
    SUMMARY_STRING = f"Have {TOTAL_OWN} out of {TOTAL_MAX} total cards for a playset " \
        f"- {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(SUMMARY_STRING, out_file_h)

    # Vintage
    vintage_dict = process_formats("Vintage", card_corrections)
    handle_output("Vintage", vintage_dict, out_file_h)

    # Legacy
    legacy_dict = process_formats("Legacy", card_corrections)
    handle_output("Legacy", legacy_dict, out_file_h)

    # Premodern
    prem_dict = process_formats("Premodern", card_corrections)
    handle_output("Premodern", prem_dict, out_file_h)

    # Modern
    modern_dict = process_formats("Modern", card_corrections)
    handle_output("Modern", modern_dict, out_file_h)

    # Pioneer
    pioneer_dict = process_formats("Pioneer", card_corrections)
    handle_output("Pioneer", pioneer_dict, out_file_h)

    # Standard
    standard_dict = process_formats("Standard", card_corrections)
    handle_output("Standard", standard_dict, out_file_h)

    # Pauper
    pauper_dict = process_formats("Pauper", card_corrections)
    handle_output("Pauper", pauper_dict, out_file_h)

    # Oathbreaker
    oath_dict = process_formats("Oathbreaker", card_corrections)
    handle_output("Oathbreaker", oath_dict, out_file_h)

    # Ice Age Block
    ia_dict = process_formats("Ice Age Block", card_corrections)
    handle_output("Ice Age Block", ia_dict, out_file_h)

    # Mirage Block
    mir_dict = process_formats("Mirage Block", card_corrections)
    handle_output("Mirage Block", mir_dict, out_file_h)

    # Tempest Block
    tem_dict = process_formats("Tempest Block", card_corrections)
    handle_output("Tempest Block", tem_dict, out_file_h)

    # Urza's Block
    urz_dict = process_formats("Urza's Block", card_corrections)
    handle_output("Urza's Block", urz_dict, out_file_h)

    # Masques Block
    masques_dict = process_formats("Masques Block", card_corrections)
    handle_output("Masques Block", masques_dict, out_file_h)

    # Invasion Block
    invasion_dict = process_formats("Invasion Block", card_corrections)
    handle_output("Invasion Block", invasion_dict, out_file_h)

    # Odyssey Block
    odys_dict = process_formats("Odyssey Block", card_corrections)
    handle_output("Odyssey Block", odys_dict, out_file_h)

    # Onslaught Block
    ons_dict = process_formats("Onslaught Block", card_corrections)
    handle_output("Onslaught Block", ons_dict, out_file_h)

    # Mirrodin Block
    mir_dict = process_formats("Mirrodin Block", card_corrections)
    handle_output("Mirrodin Block", mir_dict, out_file_h)

    # Kamigawa Block
    kam_dict = process_formats("Kamigawa Block", card_corrections)
    handle_output("Kamigawa Block", kam_dict, out_file_h)

    # Ravnica Block
    rav_dict = process_formats("Ravnica Block", card_corrections)
    handle_output("Ravnica Block", rav_dict, out_file_h)

    # Pauper Commander
    paup_comm = process_formats("Pauper Commander", card_corrections)
    handle_output("Pauper Commander", paup_comm, out_file_h)

    # Commander
    comm_dict = process_formats("Commander", card_corrections)
    handle_output("Commander", comm_dict, out_file_h)

    double_print("\nDecks for various Commander Color IDs:", out_file_h)
    deck_ids_used = set()
    for deck in comm_dict['DECKS']:
        color_id = deck[0].split('/')[0]
        if color_id in deck_ids_used:
            continue
        deck_ids_used.add(color_id)
        deck_commander = deck[0].split('/')[1]
        deck_need_num = deck[1]
        deck_need_cards = deck[2]
        double_print(f"Color Combo: {color_id}, Commander: {deck_commander}", out_file_h)
        double_print(f"Needed cards: {deck_need_num} - {str(deck_need_cards)}\n", out_file_h)

    for deck in comm_dict['DECKS']:
        if deck[0] in commander_cats['Marvel']:
            double_print(f"Marvel deck closest to completion: {deck[0]}", out_file_h)
            double_print(f"Needed cards: {deck[1]} - {str(deck[2])}\n", out_file_h)
            break
    for deck in comm_dict['DECKS']:
        if deck[0] in commander_cats['Warhammer 40K']:
            double_print(f"Warhammer 40K deck closest to completion: {deck[0]}", out_file_h)
            double_print(f"Needed cards: {deck[1]} - {str(deck[2])}\n", out_file_h)
            break
    for deck in comm_dict['DECKS']:
        if deck[0] in commander_cats['Lord of the Rings']:
            double_print(f"Lord of the Rings deck closest to completion: {deck[0]}", out_file_h)
            double_print(f"Needed cards: {deck[1]} - {str(deck[2])}\n", out_file_h)
            break
    for deck in comm_dict['DECKS']:
        if deck[0] in commander_cats['Final Fantasy']:
            double_print(f"Final Fantasy deck closest to completion: {deck[0]}", out_file_h)
            double_print(f"Needed cards: {deck[1]} - {str(deck[2])}\n", out_file_h)
            break
    for deck in comm_dict['DECKS']:
        if deck[0] in commander_cats['Other']:
            double_print(f"Other U.B. deck closest to completion: {deck[0]}", out_file_h)
            double_print(f"Needed cards: {deck[1]} - {str(deck[2])}\n", out_file_h)
            break

    print_deck = comm_dict["OLDEST"]
    old_name = print_deck[1].replace('.txt','')
    updated = datetime.datetime.strftime(print_deck[0], "%m/%d/%Y")
    double_print(f"Oldest Commander deck is {old_name}, last updated {updated}", out_file_h)

    print_deck = oath_dict["OLDEST"]
    old_name = print_deck[1].replace('.txt','')
    updated = datetime.datetime.strftime(print_deck[0], "%m/%d/%Y")
    double_print(f"Oldest Oathbreaker deck is {old_name}, last updated {updated}\n", out_file_h)

    # Other
    del creature_types['Forest']
    del creature_types['Saga']
    one_ofs = []
    for creature, creature_freq in creature_types.items():
        if creature_freq == 1:
            one_ofs.append(creature)
    double_print("*** OTHER DATA ***", out_file_h)
    double_print(f"{len(creature_types)} total creature types", out_file_h)
    USED_TYPES = ['Wall', 'Necron', 'Human', 'Cleric', 'Goblin', 'Squirrel', 'Soldier', 'Sliver',
        'Wizard', 'Spider', 'Barbarian', 'Beast', 'Zombie', 'Elf', 'Warrior', 'Spirit', ]
    for del_type in USED_TYPES:
        del creature_types[del_type]
    creature_types = sorted(creature_types.items(), key=lambda x:(-1 * x[1], x[0]))
    if creature_types[99][1] >= len(USED_TYPES) - 5:
        double_print(f"Time to do a Tribal Commander - {creature_types[0][0]}", out_file_h)
    remove_one_ofs = ['Spawn', 'Oyster', 'Ferret', 'Seal']
    for remove_type in remove_one_ofs:
        try:
            one_ofs.remove(remove_type)
        except ValueError:
            print(f"{remove_type} is no longer a true one-of")
    if len(one_ofs) > 0:
        double_print("Following creature types have only one entry:", out_file_h)
        double_print(str(sorted(one_ofs)), out_file_h)

    double_print(f"\n{len(planeswalkers)} total Planeswalkers in the game.", out_file_h)
    double_print(f"{PLANESWALKER_COUNT} total Planeswalker cards in the game.", out_file_h)
    for pw_name, pw_cards in sorted(planeswalkers.items()):
        pw_str = f"{pw_name} ({len(pw_cards)}): {'; '.join(sorted(pw_cards))}"
        double_print(pw_str, out_file_h)

    double_print("\nPercentages ordered by format:", out_file_h)
    FORMAT_LIST = sorted(FORMAT_LIST, key=lambda x:(x[1]/x[2], x[0]), reverse=True)
    for print_format in FORMAT_LIST:
        double_print(f"{print_format[0]}: {100 * print_format[1]/print_format[2]:.2f}", out_file_h)

    print(f"\nShould be {CHECK_AMOUNT} for {CHECK_SET}: {SET_CHECK}")

    double_print(f"\nFirst card needing a mana value is {FIRST_MANA_NEEDED_CARD}", out_file_h)
    MANA_DONE = MANA_CARDS_DONE/len(raw_list) * 100
    double_print(f"Currently done with {MANA_CARDS_DONE} cards - {MANA_DONE:.2f} pct", out_file_h)

    out_file_h.close()
