#!/usr/bin/python3

"""
Deck play suggestor, W-L Tracker for KeyForge
"""

import os

valid_houses = ['Brobnar', 'Mars', 'Untamed', 'Logos', 'Sanctum', 'Shadows', 'Star Alliance',
    'Dis', 'Saurian Republic', 'Unfathomable', ] # Ekwidon
valid_sets = ['Call of the Archons', 'Worlds Collide', 'Age of Ascension', 'Mass Mutation',
    'Dark Tidings', ] # Winds of someting

if os.getcwd().endswith('card_games'):
    deck_info = open('wl_data/KeyForgeDecks.txt', 'r', encoding="UTF-8")
    wl_info = open('wl_data/KeyForgeWLData.txt', 'r', encoding="UTF-8")
else:
    deck_info = open('card_games/wl_data/KeyForgeDecks.txt', 'r', encoding="UTF-8")
    wl_info = open('card_games/wl_data/KeyForgeWLData.txt', 'r', encoding="UTF-8")

my_decks = []

class Deck:
    """
    Definition for a deck object, that tracks information about the contents of the deck
    as well as its performance.
    """
    def __init__(self, short_name, name, in_set, houses, notes):
        self.short_name = short_name
        self.name = name
        if in_set in valid_sets:
            self.in_set = in_set
        else:
            print('Invalid set: ' + in_set)
        self.houses = set()
        for test_house in houses.split(','):
            if test_house.strip() not in valid_houses:
                print("Invalid house: " + test_house.strip())
            else:
                self.houses.add(test_house.strip())
        self.deck_note = notes
        self.games = 0
        self.wins = 0
        self.losses = 0
    def __str__(self):
        return "Deck: %s, Houses: %s, Record: %d-%d, Note: %s" % (self.name, ', '.join(self.houses), self.wins, self.losses, self.deck_note)
    
def getDeck(name):
    for deck in my_decks:
        if deck.name == name or deck.short_name == name:
            return deck
    return None

deck_lines = deck_info.readlines()
wl_lines = wl_info.readlines()

for deck in deck_lines:
    deck_short_name, deck_name, game_set, deck_houses, deck_note = deck.split(';')
    my_decks.append(Deck(deck_short_name, deck_name, game_set, deck_houses, deck_note))
for wl in wl_lines:
    short_deck_name, games, wins = wl.split(';')
    this_deck = getDeck(short_deck_name)
    this_deck.games = int(games)
    this_deck.wins = int(wins)
    this_deck.losses = int(games) - int(wins)

# Figure out house frequencies, both ownership and plays
owned_houses = {}
played_houses = {}
for house in valid_houses:
    owned_houses[house] = 0
    played_houses[house] = 0
for deck in my_decks:
    for house in deck.houses:
        owned_houses[house] += 1
        played_houses[house] += deck.games

# Figure out set I own the least from.
# FIgure out least played deck.
# Figure out deck I'm most successful with.
# Output least owned house, and least owned set.
# Output least played deck, with number of games.
# OUput most successful deck,

if __name__ == "__main__":
    pass