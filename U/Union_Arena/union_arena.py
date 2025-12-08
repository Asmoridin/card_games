#!/usr/bin/python3

"""
Collection manager/purchase suggester for Union Arena
"""

import os

from card_games.General.Libraries.deck import Deck
from card_games.General.Libraries.output_utils import double_print
from card_games.General.Libraries.sort_and_filter import sort_and_filter

GAME_NAME = "Union Arena"

valid_types = ['Character', 'Event', 'Site']
valid_colors = ['Green', 'Yellow', 'Blue', 'Purple', 'Red']
valid_rarities = ['C', 'U', 'R', 'SR', 'SP', ]

FILE_PREFIX = "card_games\\U\\Union_Arena"
DECK_PREFIX = FILE_PREFIX + "\\Decks"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "U\\Union_Arena"

file_h = open(FILE_PREFIX + '\\Data\\Union Arena Data.txt', 'r', encoding="UTF-8")

lines = file_h.readlines()
file_h.close()
lines = [line.strip() for line in lines]

with open(FILE_PREFIX + '\\Data\\Union Arena Sets.txt', 'r', encoding="UTF-8") as in_sets:
    ua_sets = in_sets.readlines()
ua_sets = [line.strip() for line in ua_sets if line.strip() != '']

CODES_FILE_NAME = FILE_PREFIX + '\\Data\\Union Arena Source Material Codes.txt'
with open(CODES_FILE_NAME, 'r', encoding="UTF-8") as in_codes:
    temp_ua_codes = in_codes.readlines()
temp_ua_codes = [line.strip() for line in temp_ua_codes if line.strip() != '']
ua_codes = {}
for line in temp_ua_codes:
    try:
        code, source = line.split(';')
    except ValueError:
        print("Invalid line in source material codes:")
        print(line)
        continue
    ua_codes[code] = source

with open(FILE_PREFIX + '/Data/Union Arena WL Data.txt', 'r', encoding="UTF-8") as in_wl:
    ua_wl = in_wl.readlines()
ua_wl = [line.strip() for line in ua_wl if line.strip() != '']

TOTAL_OWN = 0
TOTAL_MAX = 0
item_list = []
card_inv_dict = {}
most_needed_cards = {}
card_mapping = {}
prop_color_mapping = {}
ownership_by_set_color = {}
card_codes = set()
prop_ownership = {}
for line in lines:
    if line == '' or line.startswith('#'):
        continue
    line = line.split('#')[0].strip()
    CARD_MAX = 4
    line_vals = line.split(';')
    if len(line_vals) == 11:
        try:
            card_name, card_affin, card_code, card_rarity, card_type, card_color, card_energy, \
                card_ap, card_sets, card_triggers, card_own = line.split(';')
        except ValueError:
            print("Invalid line:")
            print(line)
            continue
    elif len(line_vals) == 12:
        try:
            card_name, card_affin, card_code, card_rarity, card_type, card_color, card_energy, \
                card_ap, card_sets, card_triggers, card_own, temp_max = line.split(';')
            CARD_MAX = int(temp_max)
        except ValueError:
            print("Invalid line:")
            print(line)
            continue
    else:
        print("Invalid line:")
        print(line)
        continue

    card_affin = card_affin.split('/')

    if card_code in card_codes:
        print(f"Duplicate card code {card_code} for {card_name}")
    card_codes.add(card_code)

    card_property = ua_codes.get(card_code[:3], 'Unknown Source')
    if card_property == 'Unknown Source':
        print(f"Unknown source code {card_code[:3]} for {card_name}")
    if card_property not in prop_color_mapping:
        prop_ownership[card_property] = [0, 0]
        prop_color_mapping[card_property] = set()
        ownership_by_set_color[card_property] = {}

    CARD_ID = f"{card_name} [{card_code}]"

    if card_rarity not in valid_rarities:
        print(f"Invalid card rarity {card_rarity} for {card_name}")
    if card_type not in valid_types:
        print(f"Invalid card type {card_type} for {card_name}")
    card_colors = card_color.split('/')
    for card_color in card_colors:
        if card_color not in valid_colors:
            print(f"Invalid card color {card_color} for {card_name}")
    prop_color_mapping[card_property].update(card_colors)
    card_energy = int(card_energy) if card_energy.isdigit() else card_energy
    card_ap = int(card_ap) if card_ap.isdigit() else card_ap

    card_sets = card_sets.split('/')

    card_own = int(card_own)

    prop_ownership[card_property][0] += card_own
    prop_ownership[card_property][1] += CARD_MAX

    TOTAL_OWN += card_own
    TOTAL_MAX += CARD_MAX
    if card_own < CARD_MAX:
        most_needed_cards[CARD_ID] = CARD_MAX - card_own
    card_inv_dict[CARD_ID] = card_own
    for card_color in card_colors:
        if card_color not in ownership_by_set_color[card_property]:
            ownership_by_set_color[card_property][card_color] = 0
        ownership_by_set_color[card_property][card_color] += card_own
    card_mapping[card_code] = CARD_ID
    item_list.append((card_name, CARD_ID, card_affin, card_code, card_property, card_rarity, \
        card_type, card_colors, card_energy, card_ap, card_sets, card_triggers, card_own, CARD_MAX))

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
            DECK_CARD_NAME = ' '.join(deck_line.split(' ')[1:]).strip()
            DECK_CARD_NAME = DECK_CARD_NAME.split('/')[1]
        except ValueError:
            print(f"Invalid deck line in {deck_path}: {deck_line}")
            continue
        if DECK_CARD_NAME not in card_mapping:
            print(f"Unknown card {DECK_CARD_NAME} in deck {deck_path}")
        else:
            DECK_CARD_NAME = card_mapping[DECK_CARD_NAME]
        if DECK_CARD_NAME not in deck_dict:
            deck_dict[DECK_CARD_NAME] = 0
        deck_dict[DECK_CARD_NAME] += deck_card_qty
    this_deck = Deck(deck_file[:-4], deck_dict, {'property': deck_file[:3]})
    this_deck.update_missing_cards(card_inv_dict)
    decks.append(this_deck)

for deck in decks:
    for card_name, missing_qty in deck.deck_missing_cards.items():
        if card_name not in most_needed_cards:
            most_needed_cards[card_name] = 0
        most_needed_cards[card_name] += missing_qty

# Filter by property
chosen_property, filtered_list = sort_and_filter(item_list, 4)

# Filter by card_color
chosen_color, filtered_list = sort_and_filter(filtered_list, 7)

#Filter by set
chosen_set, filtered_list = sort_and_filter(filtered_list, 10)

#Filter by type
chosen_type, filtered_list = sort_and_filter(filtered_list, 6)

# Filter by rarity
chosen_rarity, filtered_list = sort_and_filter(filtered_list, 5)

# Choose card
chosen_card, filtered_list = sort_and_filter(filtered_list, 0)
picked_item = filtered_list[0]

# Get W-L structures working
opp_wl_dict = {}
w_l_val = [0, 0]  # [wins, losses]
my_prop_wl = {}
opp_prop_wl = {}
my_color_wl = {}
opp_color_wl = {}
my_prop_color_games = {}
for ua_line in ua_wl:
    my_prop, my_color, opp_prop, opp_color, opp_name, w_l = ua_line.split(';')
    if opp_name not in opp_wl_dict:
        opp_wl_dict[opp_name] = [0, 0]
    my_prop = ua_codes.get(my_prop, "Unknown Source")
    if my_prop == "Unknown Source":
        print(f"Unknown source code {my_prop} in W-L data")
        continue
    if my_prop not in my_prop_wl:
        my_prop_wl[my_prop] = [0, 0]
        my_prop_color_games[my_prop] = {}
    opp_prop = ua_codes.get(opp_prop, "Unknown Source")
    if opp_prop == "Unknown Source":
        print(f"Unknown source code {opp_prop} in W-L data")
        continue
    if opp_prop not in opp_prop_wl:
        opp_prop_wl[opp_prop] = [0, 0]
    if my_color not in valid_colors:
        print(f"Invalid color {my_color} in W-L data")
        continue
    if my_color not in my_color_wl:
        my_color_wl[my_color] = [0, 0]
    if my_color not in my_prop_color_games[my_prop]:
        my_prop_color_games[my_prop][my_color] = 0
    if opp_color not in valid_colors:
        print(f"Invalid color {opp_color} in W-L data")
        continue
    if opp_color not in opp_color_wl:
        opp_color_wl[opp_color] = [0, 0]
    if w_l not in ['W', 'L']:
        print(f"Invalid W/L value {w_l} in W-L data")
        continue
    my_prop_color_games[my_prop][my_color] += 1
    if w_l == 'W':
        w_l_val[0] += 1
        my_prop_wl[my_prop][0] += 1
        opp_prop_wl[opp_prop][0] += 1
        my_color_wl[my_color][0] += 1
        opp_color_wl[opp_color][0] += 1
        opp_wl_dict[opp_name][0] += 1
    else:
        w_l_val[1] += 1
        my_prop_wl[my_prop][1] += 1
        opp_prop_wl[opp_prop][1] += 1
        my_color_wl[my_color][1] += 1
        opp_color_wl[opp_color][1] += 1
        opp_wl_dict[opp_name][1] += 1

games_by_property = {}
for prop, prop_wl in my_prop_wl.items():
    games_by_property[prop] = prop_wl[0] + prop_wl[1]

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/Union Arena Out.txt", 'w', encoding="UTF-8")

    double_print("Union Arena Inventory Tracker Tool\n", out_file_h)

    total_string = f"Have {TOTAL_OWN} out of {TOTAL_MAX} - {100* TOTAL_OWN/TOTAL_MAX:.2f} percent"
    double_print(total_string, out_file_h)

    SUGG_STRING = f"Buy {picked_item[1]} ({chosen_color + ' ' + chosen_type}) from " + \
        f"{chosen_set} (have {picked_item[-2]} out of {picked_item[-1]})"
    double_print(SUGG_STRING, out_file_h)

    TOTAL_COMBOS = 0
    for prop, colors in prop_color_mapping.items():
        TOTAL_COMBOS += len(colors)
    double_print(f"\nTotal property/color combinations: {TOTAL_COMBOS}", out_file_h)

    double_print("\nMost needed cards:", out_file_h)
    sorted_most_needed = sorted(most_needed_cards.items(), key=lambda x: (-x[1], x[0]))
    for card_name, needed_qty in sorted_most_needed[:10]:
        double_print(f" - {card_mapping.get(card_name, card_name)}: {needed_qty} cards", out_file_h)

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
            CARD_STR = f"    - {card_mapping.get(card_name, card_name)}: {missing_qty}"
            double_print(CARD_STR, out_file_h)

    double_print("\nWin-Loss Information:", out_file_h)
    double_print("My record: " + f"{w_l_val[0]}-{w_l_val[1]}", out_file_h)
    double_print("Win-Loss by Property:", out_file_h)
    for prop, wl_vals in sorted(my_prop_wl.items()):
        double_print(f" - {prop}: {wl_vals[0]}-{wl_vals[1]}", out_file_h)

    double_print("Record Against Properties:", out_file_h)
    for prop, wl_vals in sorted(opp_prop_wl.items()):
        double_print(f" - {prop}: {wl_vals[0]}-{wl_vals[1]}", out_file_h)

    double_print("Win-Loss by Color:", out_file_h)
    for color, wl_vals in sorted(my_color_wl.items()):
        double_print(f" - {color}: {wl_vals[0]}-{wl_vals[1]}", out_file_h)

    double_print("Record Against Colors:", out_file_h)
    for color, wl_vals in sorted(opp_color_wl.items()):
        double_print(f" - {color}: {wl_vals[0]}-{wl_vals[1]}", out_file_h)

    double_print("Record Against Opponents:", out_file_h)
    for opp_name, wl_vals in sorted(opp_wl_dict.items()):
        double_print(f" - {opp_name}: {wl_vals[0]}-{wl_vals[1]}", out_file_h)

    playable_props = {}
    for prop_name, colors in ownership_by_set_color.items():
        for color, owned_qty in colors.items():
            if owned_qty >= 50:
                if prop_name not in playable_props:
                    playable_props[prop_name] = []
                playable_props[prop_name].append(color)
    for playable_prop in playable_props:
        if playable_prop not in games_by_property:
            games_by_property[playable_prop] = 0
    games_by_property = sorted(games_by_property.items(), key=lambda x: (x[1], x[0]))
    CHOSEN_PROP = games_by_property[0][0]
    color_chooser = {}
    for color in playable_props[CHOSEN_PROP]:
        if color not in color_chooser:
            color_chooser[color] = 0
    for color in my_prop_color_games.get(CHOSEN_PROP, {}):
        color_chooser[color] = my_prop_color_games[CHOSEN_PROP][color]
    color_chooser = sorted(color_chooser.items(), key=lambda x: (x[1], x[0]))
    CHOSEN_COLOR = color_chooser[0][0]
    double_print(f"\nSuggested property/color to play next: {CHOSEN_PROP} / {CHOSEN_COLOR}", \
        out_file_h)

    sorted_prop_ownership = sorted(prop_ownership.items(), key=lambda x: \
        (-x[1][0] / x[1][1], x[1][1] - x[1][0], x[0]))
    double_print("\nOwnership by Property:", out_file_h)
    for prop, ownership in sorted_prop_ownership:
        prop_own_str = f" - {prop}: {ownership[0]} out of {ownership[1]} " + \
            f"({100 * ownership[0]/ownership[1]:.2f} percent)"
        double_print(prop_own_str, out_file_h)

    out_file_h.close()
