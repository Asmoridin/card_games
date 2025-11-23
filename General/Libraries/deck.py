#!/usr/bin/env python3

"""
Class to represent a deck in a variety of games, with helper fuctions
"""

class Deck:
    """
    Class to represent a deck in a variety of games, with helper fuctions
    """
    def __init__(self, deck_name, cards, deck_tags=None):
        self.deck_name = deck_name
        self.cards = cards
        if deck_tags is None:
            self.deck_tags = {}
        else:
            self.deck_tags = deck_tags
    def __repr__(self):
        return f"Deck('{self.deck_name}', {self.cards}, {self.deck_tags})"
