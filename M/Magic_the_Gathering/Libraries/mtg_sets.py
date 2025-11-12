#!/usr/bin/python3

"""
Library to more easily handle MTG sets
"""

LEGACY_SETS = ["Limited Edition Alpha", "Limited Edition Beta", "Unlimited Edition", "Jumpstart",
    "Revised Edition", "Fourth Edition", "Fifth Edition", "Classic Sixth Edition", "Battlebond",
    "Double Masters 2022", "Ultimate Box Toppers", "Ultimate Masters", "Seventh Edition",
    "Masterpiece Series: Kaladesh Inventions", "Dominaria Remastered", "Jumpstart 2022", "Ice Age",
    "Eternal Masters", "Archenemy", "Commander 2016", "Commander 2015", "Commander 2013 Edition",
    "Commander Anthology 2018", "Duel Decks: Elspeth vs. Tezzeret", "Commander Anthology",
    "Duel Decks: Ajani vs. Nicol Bolas", "Magic: The Gathering-Commander", "Beatdown Box Set",
    "The Brothers' War Retro Artifacts", "From the Vault: Relics", "Bloomburrow Commander",
    "The Lord of the Rings: Tales of Middle Earth Commander", "Modern Horizons 3 Commander",
    "Outlaws of Thunder Junction Commander", "Murders at Karlov Manor Commander", "Commander 2021",
    "Magic The Gathering—Fallout", "The Lost Caverns of Ixalan Commander", "Doctor Who Commander",
    "Wilds of Eldraine Commander", "Commander Masters", "March of the Machine Commander", 
    "Phyrexia: All Will Be One Commander", "Dominaria United Commander", "Commander 2018",
    "Kamigawa: Neon Dynasty Commander", "The Brothers' War Commander", "Commander 2019",
    "Warhammer 40,000 Commander", "Commander Legends: Battle for Baldur's Gate", "Invasion", 
    "Streets of New Capenna Commander", "Commander Collection: Green", "Kaldheim Commander",
    "Adventures in the Forgotten Realms Commander", "Innistrad: Crimson Vow Commander", 
    "Innistrad: Midnight Hunt Commander", "Commander Legends", "Ikoria Commander", "Mirage",
    "Zendikar Rising Commander", "Commander 2017", "Commander 2014", "Starter 2000",
    "Secret Lair Drop", "Duel Decks Anthology, Garruk vs. Liliana", "Portal", "Masters 25",
    "Duel Decks: Garruk vs. Liliana", "Starter 1999", "Strixhaven Mystical Archive",
    "Masterpiece Series: Amonkhet Invocations", "Duel Decks Anthology, Divine vs. Demonic",
    "Duel Decks: Divine vs. Demonic", "From the Vault: Twenty", "Planechase", "Mercadian Masques",
    "Duel Decks: Phyrexia vs. the Coalition", "Battle Royale Box Set", "Urza's Saga", "Tempest",
    "Premium Deck Series: Graveborn", "Iconic Masters", "Portal Second Age", "Torment",
    "Conspiracy: Take the Crown", "Duel Decks: Sorin vs. Tibalt", "Duel Decks: Jace vs. Chandra",
    "Duel Decks Anthology, Jace vs. Chandra", "Duel Decks: Jace vs. Vraska", "Onslaught",
    "Duel Decks: Venser vs. Koth", "Signature Spellbook: Jace", "Game Night", "Special Guests",
    "Game Night: Free-For-All", "Explorers of Ixalan", "Duel Decks Anthology, Elves vs. Goblins",
    "Duel Decks: Elves vs. Goblins", "Duel Decks: Heroes vs. Monsters", "Guild Kit: Gruul",
    "Global Series: Jiang Yanggu and Mu Yanling", "From the Vault: Exiled", "Ravnica Remastered",
    "Duel Decks: Knights vs. Dragons", "From the Vault: Dragons", "Ravnica Clue Edition",
    "Premium Deck Series: Fire and Lightning", "Wilds of Eldraine Enchanting Tales",
    "Archenemy: Nicol Bolas", "Portal Three Kingdoms", "From the Vault: Annihilation (2014)",
    "Duel Decks: Izzet vs. Golgari", "Duel Decks: Merfolk vs. Goblins", "Odyssey", "Legions",
    "Duel Decks: Elspeth vs. Kiora", "Duel Decks: Mind vs. Might", "Guild Kit: Dimir", "Exodus",
    "Guild Kit: Izzet", "Guild Kit: Azorius", "Guild Kit: Simic", "Game Night 2019", "Apocalypse",
    "Duel Decks: Speed vs. Cunning", "Duel Decks: Elves vs. Inventors", "Legends", "The Dark",
    "Premium Deck Series: Slivers", "Jurassic World Collection Cards", "Chronicles", "Homelands",
    "Planechase Anthology", "Planechase 2012 Edition", "Duel Decks: Blessed vs. Cursed",
    "Unfinity", "From the Vault: Angels", "Magic: The Gathering—Conspiracy", "Guild Kit: Golgari",
    "Guild Kit: Orzhov", "Guild Kit: Rakdos", "Duel Decks: Nissa vs. Ob Nixilis", "Alliances",
    "Duel Decks: Zendikar vs. Eldrazi", "Guild Kit: Selesnya", "Guild Kit: Boros", "Visions",
    "Arabian Nights", "Time Spiral Remastered", "Judgment", "From the Vault: Realms", "Nemesis",
    "Zendikar Expeditions", "Zendikar Rising Expeditions", "Antiquities", "Commander's Arsenal",
    "Outlaws of Thunder Junction Breaking News", "March of the Machine Multiverse Legends",
    "Weatherlight", "Fallen Empires", "Promo set for Gatherer", "Urza's Legacy", "Urza's Destiny",
    "From the Vault: Transform", "Ravnica Allegiance Mythic Edition", "Stronghold", "Scourge",
    "Duskmourn: House of Horror Commander", "Signature Spellbook: Gideon", "From the Vault: Lore",
    "Ugin's Fate promos", "Planeshift", "From the Vault: Legends", "Prophecy",
    "Mystery Booster 2: Convention Edition", "Magic: The Gathering Foundations Commander",
    "Jumpstart 2025", "Innistrad Remastered", "SNC Game Day", "Aetherdrift Commander",
    "Tarkir: Dragonstorm Commander", "War of the Spark Mythic Edition", 'SNC Store Championship',
    "FINAL FANTASY Through the Ages", "Magic: The Gathering—FINAL FANTASY Commander",
    "Edge of Eternities Bonus Sheet", "Edge of Eternities Commander", 'Source Material Cards',
    "SPE - Magic: The Gathering | Marvel's Spider-Man", 'Guilds of Ravnica Mythic Edition',
    'Promo Cards', 'Universes Within',
    ]

NON_SETS = ['Unglued', "Unhinged", "Unstable", "Unsanctioned", 'Vanguard']
ARENA_SETS = ["Jumpstart: Historic Horizons", "Historic Anthology 1", "Arena Base Set",
    "Amonkhet Remastered", "Shadows Over Innistrad Remastered", "Kaladesh Remastered",
    "Alchemy Horizons: Baldur's Gate", "Historic Anthology 2", "Historical Anthology 1",
    "Shadows of the Past", "Historic Anthology 5", "Historic Anthology 3", "Historic Anthology 4",
    ]

# Sets that were only released on MTG Online.  We care about the rarity, but that's it.
MTGO_SETS = ["Vintage Masters", "Masters Edition IV", "Masters Edition III", "Masters Edition",
    "Double Masters", "Tempest Remastered", "Masters Edition II", ]

# Specific fixed set of sets for the Premodern format
PREMODERN_SETS = [
    "Fourth Edition", "Fifth Edition", "Ice Age", "Chronicles", "Homelands", "Alliances",
    "Mirage", "Visions", "Weatherlight", "Urza's Saga", "Tempest", "Stronghold", "Scourge",
    "Exodus", "Urza's Legacy", "Urza's Destiny", "Classic Sixth Edition", "Mercadian Masques",
    "Nemesis", "Prophecy", "Invasion", "Planeshift", "Seventh Edition", "Apocalypse",
    "Odyssey", "Legions", "Torment", "Judgment", "Onslaught"
]

# Standard legal sets are legal in all other formats, mostly.
STANDARD_SETS = ["Wilds of Eldraine", "The Lost Caverns of Ixalan", "Murders at Karlov Manor",
    "Outlaws of Thunder Junction", "Outlaws of Thunder Junction: The Big Score", "Bloomburrow",
    "Duskmourn: House of Horror", "Magic: The Gathering Foundations", "Aetherdrift",
    "Tarkir: Dragonstorm", "Magic: The Gathering—FINAL FANTASY", "Edge of Eternities",
    "Magic: The Gathering | Marvel's Spider-Man", "Magic: The Gathering | Avatar: The Last Airbender"]

# These sets are legal in Pioneer, Modern, and older formats
PIONEER_SETS = ["Return to Ravnica", "Gatecrash", "Dragon's Maze", "Magic 2014 Core Set", "Theros",
    "Born of the Gods", "Journey into Nyx", "Magic 2015 Core Set", "Khans of Tarkir",
    "Fate Reforged", "Dragons of Tarkir", "Magic Origins", "Battle for Zendikar",
    "Oath of the Gatewatch", "Welcome Deck 2016", "Shadows over Innistrad", "Eldritch Moon",
    "Kaladesh", "Aether Revolt", "Welcome Deck 2017", "Amonkhet", "Hour of Devastation", "Ixalan",
    "Rivals of Ixalan", "Dominaria", "Core Set 2019", "Guilds of Ravnica", "Ravnica Allegiance",
    "War of the Spark", "Core Set 2020", "Throne of Eldraine", "Theros Beyond Death",
    "Ikoria: Lair of Behemoths", "Core Set 2021", "Zendikar Rising", "Kaldheim",
    "Strixhaven: School of Mages", "Adventures in the Forgotten Realms",
    "Innistrad: Midnight Hunt", "Innistrad: Crimson Vow", "Kamigawa: Neon Dynasty",
    "Streets of New Capenna", "Dominaria United", "The Brothers' War", "Phyrexia: All Will Be One",
    "March of the Machine", "March of the Machine: The Aftermath",]

# These are legal in Modern and older formats
MODERN_SETS  = ["Eighth Edition", "Mirrodin", "Darksteel", "Fifth Dawn", "Champions of Kamigawa",
    "Betrayers of Kamigawa", "Saviors of Kamigawa", "Ninth Edition", "Ravnica: City of Guilds",
    "Guildpact", "Dissension", "Coldsnap", "Time Spiral", "Planar Chaos", "Future Sight",
    "Tenth Edition", "Lorwyn", "Morningtide", "Shadowmoor", "Eventide", "Shards of Alara",
    "Conflux", "Alara Reborn", "Magic 2010", "Zendikar", "Worldwake", "Rise of the Eldrazi",
    "Magic 2011", "Scars of Mirrodin", "Mirrodin Besieged", "New Phyrexia", "Magic 2012",
    "Innistrad", "Dark Ascension", "Avacyn Restored", "Magic 2013", "Modern Horizons 2",
    "Modern Horizons", "The Lord of the Rings: Tales of Middle Earth", "Modern Horizons 3",
    "Assassin's Creed", 'Time Spiral "Timeshifted"', "Modern Masters 2015 Edition",
    "Modern Event Deck 2014", "Modern Masters", "Modern Masters 2017 Edition",
    ]
