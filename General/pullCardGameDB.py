#!/usr/bin/python3

"""
Little module to find next set of cards in large MTG Oracle gaps
"""

import json
import pip._vendor.requests as requests
#import requests
#import requests.exceptions

def make_call():
    """
    Given a card number, make the call with the number
    Return a 1 for finding the card
    0 for not finding it
    -1 for timeout
    """
    url = 'https://www.cardgamedb.com/index.php/starwars/star-wars-deck-section/_/light/hoth-7-reserve-deck-r587'
    try:
        response = requests.get(url, timeout=5, verify=False)
        return(response.text)
    except requests.exceptions.ReadTimeout:
        return -1
    if 'Filter by:' in response.text:
        return 0
    return 1

data = make_call()
start_i = data.index('rawdeck') + 11
end_i = data.index('var viewType') - 4
data = data[start_i:end_i].replace('&quot;', '"')
this_json = json.loads(data)
print(this_json.keys())
print(this_json['objectives'])
print(this_json['affiliation'])
