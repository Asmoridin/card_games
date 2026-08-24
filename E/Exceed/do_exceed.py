#!/usr/bin/python3

"""
Script that generates groups for a future Exceed tournament
"""

import math
import os
import random

from steve_utils.output_utils import double_print

FILE_PREFIX = "card_games/E/Exceed"
if os.getcwd().endswith('card_games'):
    FILE_PREFIX = "E/Exceed"

red_horizon = ['Eva', 'Kaden', 'Miska', 'Lily', 'Reese', 'Heidi', 'Vincent', 'Nehtali',
    'Satoshi', 'Mei-Lien', 'Baelkhor', 'Morathi', 'Gabrek', 'Ulrik', 'Alice', 'Zoey', ]#16
seventh_cross = ['Geoffrey', 'Celinka', 'Taisei', "D'Janette", 'ZSolt', 'Renea', 'Minato',
    'Tournelouse', 'Eugenia', 'Galdred', 'Umina', 'Remiliss', 'Luciya', 'Syrus', 'Seijun',
    'Iaquis', 'Emogine', 'Sydney & Serena', ] #18
promo = ['Juno', 'Devris', 'Super Skull Man 33', 'Carl Swangee', 'Pooky', 'Shovel Knight',
    'Fight', 'The Beheaded'] #8
street_fighter = ['Sagat', 'Ryu', 'Akuma', 'Zangief', 'Vega', 'C.Viper', 'Chun-Li', 'Dan', 'Cammy',
    'M. Bison', 'Ken', 'Guile', ] #12
shovel_knight = ['Shovel Knight & Shield Knight', 'Propeller Knight', 'Mole Knight',
    'Tinker Knight', 'Plague Knight', 'Polar Knight', 'Treasure Knight', 'King Knight',
    'The Enchantress', 'Specter Knight', ] #10
blazblue = ['Ragna', 'Tager', 'Taokaka', 'Rachel', 'Jin', 'Hakumen', 'Carl', 'Bang', 'Noel',
    'Nu-13', 'Arakune', 'Litchi', 'Hazama', 'Nine the Phantom', 'Platinum the Trinity',
    'Kokonoe', ] #16
under_night = ['Yuzuriha', 'Carmine', 'Byakuya', 'Mika', 'Gordeau', 'Chaos', 'Hilda', 'Phonon',
    'Seth', 'Enkdu', 'Vatista', 'Nanase', 'Orie', 'Waldstein', 'Merkava', 'Wagner', 'Hyde',
    'Linne', 'Londrekia', ] #19
guilty_gear = ['Sol Badguy', 'Ky Kiske', 'May', 'Axl Low', 'Chipp Zanuff', 'Potemkin', 'Faust',
    'Millia Rage', 'Zato-1', 'Ramlethal Valentine', 'I-No', 'Nagoriyuki', 'Giovanna', 'Anji Mito',
    'Leo Whitefang', 'Jack-O', 'Goldlewis Dickinson', 'Happy Chaos', 'Baiken', 'Testament', ] # 20

fighters = sorted(red_horizon + seventh_cross + promo + street_fighter + shovel_knight + \
    blazblue + under_night + guilty_gear)

def gen_groups(number_of_groups):
    """
    Generate a number of random groups, with the only input being the desired number of groups
    """
    groups = []
    for group_name in [red_horizon, seventh_cross, promo, street_fighter, shovel_knight, blazblue,
            under_night, guilty_gear]:
        random.shuffle(group_name)
    fighter_order = red_horizon + seventh_cross + promo + street_fighter + shovel_knight + \
        blazblue + under_night + guilty_gear
    for group_num in range(0, number_of_groups):
        this_group = []
        counter = group_num
        while counter <len(fighters):
            this_group.append(fighter_order[counter])
            counter += number_of_groups
        groups.append(this_group)
    return groups

if __name__ == "__main__":
    out_file_h = open(FILE_PREFIX + "/ExceedOut.txt", 'w', encoding="UTF-8")
    for group in gen_groups(8):
        print(group)
    summ_str = f"\nTotal: {len(fighters)} Fighters, and {math.comb(len(fighters), 2)} combinations"
    double_print(summ_str, out_file_h)
