#!/usr/bin/python3

"""
Little module to find next set of cards in large MTG Oracle gaps
"""


import time
import os
import pip._vendor.requests as requests
#import requests
#import requests.exceptions

def make_call(number):
    """
    Given a card number, make the call with the number
    Return a 1 for finding the card
    0 for not finding it
    -1 for timeout
    """
    url = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + str(number)
    try:
        response = requests.get(url, timeout=5, verify=False)
    except requests.exceptions.ReadTimeout:
        return -1
    if 'Filter by:' in response.text:
        return 0
    return 1

for x in range(63761, 900000):
    time.sleep(1)
    RESULT = make_call(x)
    if RESULT == -1:
        print("Retrying once")
        RESULT = make_call(x)
    if RESULT == -1:
        print("Retrying twice")
        RESULT = make_call(x)
    if RESULT == -1:
        print("Failed to call: " + str(x))
        os._exit(0)
    if RESULT == 0:
        print("Nope: " + str(x))
        continue
    print("Found one: " + str(x))
    os._exit(0)
