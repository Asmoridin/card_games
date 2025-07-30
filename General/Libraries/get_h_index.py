#!/usr/bin/python3

"""
Simple function that takes in a list of (item, number) tuples, and returns the h-index
"""

def get_h_index(tuple_list):
    """
    Takes in a list of items, and returns the h-index

    This is the number, x, of items where I have x or more plays.

    For example, this list has an h-index of three:
    ('item 1', 1), ('item 2', 3), ('item 3', 5), ('item 4', 2), ('item 5', 7)
    """
    h_index = 0
    for _, total_games in enumerate(tuple_list):
        h_index += 1
        if not total_games[1] >= h_index:
            h_index -= 1
            break
    return h_index
