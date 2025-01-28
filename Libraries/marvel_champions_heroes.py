#!/usr/bin/python3

"""
Class to represent a hero, and aid in generating valid aspect combinations for the hero.
"""

import itertools

aspects = ['Leadership', 'Justice', 'Protection', 'Aggression', "'Pool"]

class Hero:
    """
    data about a hero, including name, and the ability to generate aspect combinations
    """
    def __init__(self, name, num_aspects=1):
        self.name = name
        if type(num_aspects) != type(0):
            raise ValueError('Invalid aspect count')
        self.num_aspects = num_aspects
    def gen_combos(self):
        """
        Generate all of the valid hero/aspect combinations for a particular hero.
        """
        ret_list = []
        aspect_combos = itertools.combinations(aspects, self.num_aspects)
        for aspect_combo in aspect_combos:
            ret_list.append((self.name, tuple(sorted(aspect_combo))))
        return ret_list

heroes = []
heroes.extend([
    Hero('Black Panther'), Hero('Captain Marvel'), Hero('Iron Man'), Hero('She-Hulk'),
    Hero('Spider-Man'), Hero('Captain America'), Hero('Ms. Marvel'), Hero('Thor'),
    Hero('Black Widow'), Hero('Dr. Strange'), Hero('Hulk'), Hero('Hawkeye'),
    Hero('Spider-Woman', 2), Hero('Ant-Man'), Hero('Wasp'), Hero('Quicksilver'),
    Hero('Scarlet Witch'), Hero('Groot'), Hero('Rocket Racoon'), Hero('Star-Lord'), Hero('Gamora'),
    Hero('Drax'), Hero('Venom'), Hero('Spectrum'), Hero('Adam Warlock', 4), Hero('Nebula'),
    Hero('War Machine'), Hero('Vision'), Hero('Valkyrie'), Hero('Spider-Man (Miles Morales)'),
    Hero('Ghost-Spider'), Hero('Nova'), Hero('Ironheart'), Hero('Spider-Ham'), Hero('Sp//Dr'),
    Hero('Colossus'), Hero('Shadowcat'), Hero('Cyclops'), Hero('Phoenix'), Hero('Wolverine'),
    Hero('Storm'), Hero('Gambit'), Hero('Rogue'), Hero('Cable'), Hero('Domino'), Hero('Psylocke'),
    Hero('Angel'), Hero('X-23'), Hero('Deadpool'), Hero('Bishop'), Hero('Magik'), Hero('Iceman'),
    Hero('Jubilee'), Hero('Nightcrawler'), Hero('Magneto'), #Hero('Maria Hill'), Hero('Nick Fury'),
    #Hero('Black Panther (Shuri)')
])

hero_combinations = []
for hero in heroes:
    hero_combinations.extend(hero.gen_combos())

hero_map = {}
for hero in heroes:
    hero_map[hero.name] = hero

if __name__=="__main__":
    print(hero_combinations)
