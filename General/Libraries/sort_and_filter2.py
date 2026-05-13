#!/usr/bin/env python3

"""
Sorting and filtering of card collection data.

Works with Card dataclass instances (and subclasses) from card.py.
The caller provides a key_func to extract the attribute to group by,
rather than relying on positional tuple indices.
"""

from typing import Callable

from card_games.General.Libraries.card import Card


def sort_and_filter(
    in_list: list[Card],
    key_func: Callable[[Card], str | list[str]],
    verbose: bool = False,
    by_len: bool = False,
    force_choice: str | None = None,
) -> tuple[str, list[Card]]:
    """
    Find the least-complete category in a card list and return it along
    with the cards that belong to it.

    The function groups cards by the value returned by key_func, computes
    a completion ratio for each group (owned / max_copies), and returns
    the group with the lowest ratio — i.e. the category most in need of
    attention. Within tied ratios it prefers larger groups (more cards
    still missing), then alphabetical order.

    Args:
        in_list:      Non-empty list of Card instances to sort and filter.
        key_func:     Callable that takes a Card and returns either a single
                      string (e.g. card.card_type) or a list of strings
                      (e.g. card.sets, card.rarities). Multi-value fields
                      cause the card to be counted once per value.
        verbose:      If True, print the full category ranking before
                      returning.
        by_len:       If True, and key_func returns a list, further filter
                      the result to only cards whose list has the minimum
                      length — i.e. cards that appear in the fewest sets.
        force_choice: If provided, skip the ranking and filter directly to
                      this category value instead.

    Returns:
        A tuple of (chosen_category, filtered_card_list).

    Raises:
        ValueError: If in_list is empty.
    """
    if not in_list:
        raise ValueError("in_list must not be empty")

    # Determine whether key_func returns a multi-value field
    sample_value = key_func(in_list[0])
    is_list = isinstance(sample_value, (list, tuple))

    # Build a map of category -> [total_owned, total_max]
    category_map: dict[str, list[int]] = {}
    for card in in_list:
        value = key_func(card)
        categories: list[str] = value if isinstance(value, list) else [value]
        for category in categories:
            if category not in category_map:
                category_map[category] = [0, 0]
            category_map[category][0] += card.owned
            category_map[category][1] += card.max_copies

    # Rank categories by completion ratio (ascending), then missing count
    # (descending), then name (ascending) as a tiebreaker
    ranked = sorted(
        [
            (name, totals[0] / totals[1], totals[1] - totals[0])
            for name, totals in category_map.items()
        ],
        key=lambda x: (x[1], -x[2], x[0]),
    )

    if verbose:
        print(ranked)

    chosen = force_choice if force_choice is not None else ranked[0][0]

    # Filter the card list down to the chosen category
    if is_list:
        filtered = [card for card in in_list if chosen in key_func(card)]
    else:
        filtered = [card for card in in_list if key_func(card) == chosen]

    # Optionally narrow further to cards with the shortest list value
    # (e.g. cards that appear in only one set)
    if by_len and is_list:
        min_len = min(len(key_func(card)) for card in filtered)
        filtered = [card for card in filtered if len(key_func(card)) == min_len]

    return (chosen, filtered)
