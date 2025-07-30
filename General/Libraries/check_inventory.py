#!/usr/bin/python3

"""
System to compare and manage inventory in a general way.  Good for minis and card games.
"""

def check_inventory(in_lists, inventory_dict):
    """
    Given:
    - a list of dicts, representing decks or army builds
    - a dict, representing the inventory of this product
    Return:
    - a list of tuples that are [LIST_NAME], [MISSING_NO], [MISSING_ITEMS]
    """
    ret_list = []
    clean_inventory_dict = {}

    # First, create some fuzzy entries, to handle various accents and such
    for in_item, in_item_qty in inventory_dict.items():
        clean_inventory_dict[in_item] = in_item_qty
        cleanup_rules = {'û':'u', 'ó':'o'}
        clean_name = in_item
        for start_letter, change_letter in cleanup_rules.items():
            clean_name = clean_name.replace(start_letter, change_letter)
        clean_inventory_dict[clean_name] = in_item_qty
    for c_item in in_lists:
        this_list_missing = 0
        this_list_miss_items = {}
        for item_name, item_count in c_item["list"].items():
            if item_name in clean_inventory_dict:
                if item_count > clean_inventory_dict[item_name]:
                    this_list_missing += item_count - clean_inventory_dict[item_name]
                    this_list_miss_items[item_name] = item_count - clean_inventory_dict[item_name]
            else:
                print(f"Missing item ({item_name}) in {c_item['name']}")
                this_list_missing += item_count
                this_list_miss_items[item_name] = item_count
        ret_list.append((c_item["name"], this_list_missing, this_list_miss_items))
    return ret_list
