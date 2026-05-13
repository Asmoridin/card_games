#!/usr/bin/env python3

"""
Base Card dataclass and game-specific subclasses.
 
All game scripts should import and subclass Card to represent their
card data. The base class contains fields common to every game;
subclasses add game-specific attributes like faction, rarity, cost, etc.
 
Usage:
    from card_games.General.Libraries.card import Card
 
    @dataclass
    class MyGameCard(Card):
        faction: str = ""
        rarity: str = ""
"""

from dataclasses import dataclass

@dataclass
class Card:
    """
    Base representation of a collectible card.
 
    Attributes:
        name:       Canonical card name, used as the unique identifier across
                    all data files and deck lists.
        sets:       List of set codes this card appears in. A card may appear
                    in multiple sets (e.g. a reprint).
        owned:      Number of copies currently in the collection.
        max_copies: Maximum copies needed for a complete playset. Typically 3
                    or 4, but may be 1 for unique/legendary cards.
    """
    name: str
    sets: list[str]
    owned: int
    max_copies: int

    @property
    def is_complete(self) -> bool:
        """True if the collection has a full playset of this card."""
        return self.owned >= self.max_copies

    @property
    def missing(self) -> int:
        """Number of copies still needed to complete the playset."""
        return max(0, self.max_copies - self.owned)

    @property
    def completion_ratio(self) -> float:
        """Owned copies as a fraction of max_copies. Always in [0.0, 1.0]."""
        if self.max_copies == 0:
            return 1.0
        return min(1.0, self.owned / self.max_copies)

    def __str__(self) -> str:
        return f"{self.name} ({self.owned}/{self.max_copies})"
