# Card Games Index

A comprehensive index of card games that require pre-game deck construction, similar to Magic the Gathering. This could include CCGs, TCGs, LCGs, ECGs.. basically, if you have a pool of cards, and build a deck, it belongs.

This repo is mostly about my own collection and experience playing games, but it wouldn't be difficult for someone else to use it for their needs as well.

## Structure

Games are organized alphabetically by first letter:
- **Folders 0-9**: Games starting with numbers
- **Folders A-Z**: Games organized by first letter (e.g., Magic: The Gathering is in `M/Magic_The_Gathering`)
- **General**: Items that aren't related to a single game- for instance libraries used by multiple scripts.

## Contents per Game

Each game folder contains:
- `Data/` — Game data, card lists, set lists
- `Decks/` - Decks for the game, usually split up by format
- `Libraries/` - If a game requires additional libraries, they are included here
- `Metadata/` - I will be including a yaml file here with information about a game
- `Rules/` — Rulebook and official documentation, errata, rulings
- The base level of the directory will have a script that produces an output (also in that base level) which will include information about my collection, gameplay win-loss record, analysis of the card pool, and the like

## Current Games

[You could list some here, or leave this for later]

## Contributing

To add a new game:
1. Create a folder under the appropriate letter: `[Letter]/[Game_Name]`
2. Add relevant data, scripts, and documentation
3. Follow the structure above
