#!/usr/bin/env python3

"""
Class to represent a deck in a variety of games, with helper fuctions
"""

class Deck:
    """
    Class to represent a deck in a variety of games, with helper fuctions
    """
    def __init__(self, deck_name:str, cards:dict, deck_tags:dict | None =None):
        self.deck_name = deck_name
        self.cards = cards
        if deck_tags is None:
            self.deck_tags = {}
        else:
            self.deck_tags = deck_tags
        self.deck_missing_cards = cards.copy()
    def update_missing_cards(self, card_inventory:dict):
        """
        Update the missing cards based on a given inventory

        :param card_inventory: A dict of card name to number owned
        """
        self.deck_missing_cards = {}
        for card_name, required_qty in self.cards.items():
            owned_qty = card_inventory.get(card_name, 0)
            missing_qty = required_qty - owned_qty
            if missing_qty > 0:
                self.deck_missing_cards[card_name] = missing_qty
    def get_num_missing_cards(self):
        """
        Return the total number of cards missing for this deck
        """
        return sum(self.deck_missing_cards.values())
    def __repr__(self):
        return f"Deck('{self.deck_name}', {self.cards}, {self.deck_tags})"
