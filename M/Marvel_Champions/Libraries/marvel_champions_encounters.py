#!/usr/bin/python3

"""
Contains information about the various Encounters in Marvel Champions
"""

import itertools

modular_encounters = ['Bomb Scare', 'Masters of Evil', 'Under Attack', 'Legions of Hydra',
    'The Doomsday Chair', 'A Mess of Things', 'Goblin Gimmicks', 'Power Drain',
    'Running Interference', 'Hydra Assault', 'Weapon Master', 'Hydra Patrol', 'Master of Time',
    'Anachronauts', 'Temporal', 'Kree Fanatic', 'Experimental Weapons',
    'Band of Badoon', 'Galactic Artifacts', 'Kree Militants', 'Menagerie Medley', 'Space Pirates',
    'Badoon Headhunter', 'Power Stone', 'Ship Command', 'Infinity Gauntlet', 'Black Order',
    'Armies of Titan', 'Children of Thanos', 'Legions of Hel', 'Frost Giants', 'Enchantress', 
    'Beasty Boys', 'Mister Hyde', 'Sinister Syndicate', "Crossfire's Crew", 'Wrecking Crew',
    'Ransacked Armory', 'State of Emergency', 'Streets of Mayhem', 'Brothers Grimm',
    'Guerilla Tactics', 'Sinister Assault', 'City in Chaos', 'Down to Earth', 'Symbiotic Strength',
    'Personal Nightmare', 'Whispers of Paranoia', 'Goblin Gear', 'Osborn Tech', 'Armadillo',
    'Zzzax', 'The Inheritors', "Iron Spider's Sinister Six", 'Deathstrike', 'Shadow King',
    'Exodus', 'Reavers', 'Zero Tolerance', 'Sentinels', 'Future Past', 'Brotherhood', 'Mystique',
    'Acolytes', 'Military Grade', 'Mutant Slayers', 'Nasty Boys', 'Black Tom Cassidy', 'Flight',
    'Super Strength', 'Telepathy', 'Extreme Measures', 'Mutant Insurrection', 'Infinites',
    'Dystopian Nightmare', 'Hounds', 'Dark Riders', 'Blue Moon', 'Genosha', 'Savage Land',
    'Celestial Tech', 'Clan Akkaba', 'Sauron', 'Arcade', 'Crazy Gang', 'Hellfire',
    'A.I.M. Abduction', 'A.I.M. Science', "Batroc's Brigade", 'Scientist Supreme', 'S.H.I.E.L.D.',
	'Trickster Magic',
]
mojo_encounters = ['Crime', 'Fantasy', 'Horror', 'Sci-Fi', 'Sitcom', 'Western']
thunderbolt_encounters = ['Gravitational Pull', 'Hard Sound', 'Pale Little Spider',
    'Power of the Atom', 'Supersonic', 'Batroc', 'Growing Strong', 'Extreme Risk', 'Techno',
    'Whiteout',]
reg_encounters = ['Mighty Avengers', 'The Initiative', 'Maria Hill', 'Dangerous Recruits',
    'Cape-Killer', 'Martial Law', 'Heroes for Hire', 'Paladin']
reg_stage_1 = ['Cut Off Support', 'S.H.I.E.L.D. Recruits', 'Homeland Security', 'Public Outrage', ]
reg_stage_2 = ['Negative Zone Prison', 'Hunting Rebel Heroes', 'The Initiative', 'No Going Back', ]
res_encounter = ['New Avengers', 'Secret Avengers', 'Namor', 'Atlanteans', 'Spider-Man',
    'Defenders', "Hell's Kitchen", 'Cloak & Dagger', ]
res_stage_1 = ['Gathering Support', 'Open Rebellion', 'Rallying Call', 'Going Underground', ]
res_stage_2 = ['Secret Avengers', 'Neighborhood Protectors', 'Guerilla Warfare',
    'Superhero Jailbreak', ]
all_modular_encounters = list(set(modular_encounters + mojo_encounters + thunderbolt_encounters + \
    reg_encounters + res_encounter))
reg_usable_encounters = list(set(modular_encounters + mojo_encounters + thunderbolt_encounters + \
    reg_encounters))
res_usable_encounters = list(set(modular_encounters + mojo_encounters + thunderbolt_encounters + \
    res_encounter))
modular_encounters = all_modular_encounters

encounters = []
def get_req_by_encounter(encounter_set):
    """
    For a particular encounter set, return the required encounters
    """
    for check_encounter in encounters:
        if check_encounter.name == encounter_set:
            return check_encounter.required_encounters
    return []

class Encounter:
    """
    Objects that handle all the information for an encounter, including valid/choices for
    modular encounter sets
    """
    def __init__(self, name, num_encounters, required_enc=None, can_infinity=True, \
        mojo_only=False, thunderbolt_only=False, reg=None):
        self.name = name
        if type(num_encounters) != type(0):
            raise ValueError("Invalid modular encounter count")
        self.num_encounters = num_encounters
        if required_enc is None:
            required_enc = []
        self.required_encounters = required_enc
        for this_encounter in self.required_encounters:
            if this_encounter not in all_modular_encounters:
                raise ValueError("Invalid required encounter: " + this_encounter)
        self.can_infinity = can_infinity
        self.mojo_only = mojo_only
        self.thunderbolt_only = thunderbolt_only
        self.reg = reg
    def gen_combos(self):
        """
        Generate all possible combos for this particular Encounter.
        """
        ret_list = []
        if self.name == 'The Hood':
            return []
        if self.mojo_only:
            modular_combos = itertools.combinations(mojo_encounters, self.num_encounters)
        elif self.thunderbolt_only:
            modular_combos = itertools.combinations(thunderbolt_encounters, self.num_encounters)
        elif self.reg == 'Registration':
            modular_combos = itertools.combinations(reg_usable_encounters, self.num_encounters)
        elif self.reg == 'Resistance':
            modular_combos = itertools.combinations(res_usable_encounters, self.num_encounters)
        else:
            modular_combos = itertools.combinations(all_modular_encounters, self.num_encounters)
        for modular_combo in modular_combos:
            valid = True
            for req_enc in self.required_encounters:
                if req_enc in modular_combos:
                    valid = False
            if not self.can_infinity and 'Infinity Gauntlet' in modular_combo:
                valid = False
            if valid:
                ret_list.append((self.name, tuple(sorted(modular_combo))))
        return ret_list

encounters.extend([
  Encounter('Rhino', 1),
  Encounter('Klaw', 1),
  Encounter('Ultron', 1),
  Encounter('Risky Business', 1),
  Encounter('Mutagen Formula', 1),
  Encounter('The Wrecking Crew', 0),
  Encounter('Crossbones', 3, ['Experimental Weapons']),
  Encounter('Absorbing Man', 1),
  Encounter('Taskmaster', 1, ['Hydra Patrol']),
  Encounter('Zola', 1),
  Encounter('Red Skull', 2),
  Encounter('Kang', 1),
  Encounter('Brotherhood of Badoon', 1, ['Ship Command']),
  Encounter('Infiltrate the Museum', 1, ['Galactic Artifacts']),
  Encounter('Escape the Museum', 1, ['Galactic Artifacts', 'Ship Command']),
  Encounter('Nebula', 1, ['Power Stone', 'Ship Command']),
  Encounter('Ronan the Accuser', 1, ['Power Stone', 'Ship Command']),
  Encounter('Ebony Maw', 2),
  Encounter('Tower Defense', 1, can_infinity=False),
  Encounter('Thanos', 2, ['Infinity Gauntlet']),
  Encounter('Hela', 2),
  Encounter('Loki', 2, ['Infinity Gauntlet']),
  Encounter('The Hood', 7),
  Encounter('Sandman', 1, ['City in Chaos']),
  Encounter('Venom', 1, ['Symbiotic Strength']),
  Encounter('Mysterio', 1, ['Personal Nightmare']),
  Encounter('The Sinister Six', 0, ['Guerilla Tactics'], can_infinity=False),
  Encounter('Venom Goblin', 1, ['Symbiotic Strength']),
  Encounter('Sabretooth', 2, []),
  Encounter('Project Wideawake', 1, ['Zero Tolerance']),
  Encounter('Master Mold', 1, ['Sentinels']),
  Encounter('Mansion Attack', 1, ['Brotherhood'], False),
  Encounter('Magneto', 1),
  Encounter('MaGog', 1),
  Encounter('Spiral', 3, mojo_only=True),
  Encounter('Mojo', 3, mojo_only=True),
  Encounter('Morlock Siege', 2),
  Encounter('On the Run', 2, ['Mutant Slayers']),
  Encounter('Juggernaut', 1),
  Encounter('Mister Sinister', 1, ['Flight', 'Super Strength', 'Telepathy',]),
  Encounter('Stryfe', 2),
  Encounter('Unus', 1, ['Infinites']),
  Encounter('Four Horsemen', 2, can_infinity=False),
  Encounter('Apocalypse', 2),
  Encounter('Dark Beast', 1, ['Blue Moon', 'Genosha', 'Savage Land']),
  Encounter('En Sabah Nur', 2),
  Encounter('Black Widow', 2),
  Encounter('Batroc', 2),
  Encounter('M.O.D.O.K.', 1),
  Encounter('Thunderbolts', 3, thunderbolt_only=True),
  Encounter('Baron Zemo', 2),
  Encounter('Enchantress', 1),
  Encounter('God of Lies', 1),
  Encounter('Iron Man', 4, reg="Registration"),
  Encounter('Captain Marvel', 4, reg="Registration"),
  Encounter('Captain America', 4, reg="Resistance"),
  Encounter('Spider-Woman', 4, reg="Resistance"),
])

encounter_map = {}
for encounter in encounters:
    encounter_map[encounter.name] = encounter
