from random import randrange as rand

# Your Team
Infernape = {
    'name': 'Infernape',
    'item': 'Expert Belt',
    'nature': 'Jolly',
    'evs': [0, 252, 0, 0, 4, 252],
    'boosts': None,
    'strategy': 'Sweeper',
    'moves': ['Vacuum Wave', 'Bulk Up', 'Fire Punch', 'Close Combat']
}

Alakazam = {
    'name': 'Alakazam',
    'item': 'Alakazite',
    'nature': 'Timid',
    'evs': [4, 0, 0, 252, 0, 252],
    'boosts': None,
    'strategy': 'Wall Breaker',
    'moves': ['Psychic', 'Shadow Ball', 'Energy Ball', 'Dazzling Gleam']
}

Excadrill = {
    'name': 'Excadrill',
    'item': 'Air Balloon',
    'nature': 'Adamant',
    'evs': [252, 252, 0, 0, 0, 4],
    'boosts': None,
    'strategy': 'Wall Breaker',
    'moves': ['Earthquake', 'Iron Head', 'Rock Slide', 'Brick Break']
}

Toxapex = {
    'name': 'Toxapex',
    'item': 'Black Sludge',
    'nature': 'Calm',
    'evs': [252, 0, 4, 0, 252, 0],
    'boosts': None,
    'strategy': 'Wall',
    'moves': ['Scald', 'Haze', 'Recover', 'Toxic']
}

# Team1 = [Infernape, Alakazam, Toxapex]
Team1 = [Infernape, Alakazam, Excadrill]

# Opponent Team
Houndoom = {
    'name': 'Houndoom',
    'item': 'Houndoominite',
    'nature': 'Timid',
    'evs': [0, 0, 4, 252, 0, 252],
    'boosts': None,
    'strategy': 'Wall Breaker',
    'moves': ['Flamethrower', 'Dark Pulse', 'Sludge Bomb', 'Shadow Ball']
}

Gyarados = {
    'name': 'Gyarados',
    'item': 'Leftovers',
    'nature': 'Jolly',
    'evs': [0, 248, 4, 0, 4, 252],
    'boosts': None,
    'strategy': 'Wall Breaker',
    'moves': ['Bounce', 'Waterfall', 'Earthquake', 'Crunch']
}

Zapdos = {
    'name': 'Zapdos',
    'item': 'Leftovers',
    'nature': 'Bold',
    'evs': [252, 0, 184, 0, 0, 72],
    'boosts': None,
    'strategy': 'Wall Breaker',
    'moves': ['Discharge', 'Heat Wave', 'Roost', 'Extrasensory']
}

Team2 = [Houndoom, Gyarados, Zapdos]

STAT_MAP = {
    'HP': 0,
    'Atk': 1,
    'Def': 2,
    'SpA': 3,
    'SpD': 4,
    'Spe': 5
}


def parse_pokemon(path="../documents/pokemon.txt"):
    pokemon_list = []
    Pokemon = {
        'name': 'pokemon',
        'item': 'none',
        'nature': 'none',
        'evs': [0, 0, 0, 0, 0, 0],
        'boosts': None,
        'strategy': 'None',
        'moves': []
    }

    f = open(path)
    for line in f:
        line = line.replace('\n', '')
        if '@' in line:
            temp = line.split()
            Pokemon['name'] = temp[0]
            Pokemon['item'] = ' '.join(temp[2:])
        elif 'EVs' in line:
            temp = line[4:].replace('/', '').split()
            for t in range(len(temp)):
                if temp[t] in STAT_MAP.keys():
                    Pokemon['evs'][STAT_MAP[temp[t]]] = temp[t - 1]
        elif 'Nature' in line:
            Pokemon['nature'] = line[:-7]
        elif 'Strategy' in line:
            Pokemon['strategy'] = line[10:]
        elif '-' in line:
            Pokemon['moves'].append(line[2:])
        elif '#' in line:
            pokemon_list.append(Pokemon)
            Pokemon = {
                'name': 'pokemon',
                'item': 'none',
                'nature': 'none',
                'evs': [0, 0, 0, 0, 0, 0],
                'boosts': None,
                'strategy': 'None',
                'moves': []
            }
    return pokemon_list


def team_gen(path="../documents/pokemon.txt"):
    pp = parse_pokemon
    pool = pp(path)
    TeamY = []
    TeamO = []

    for x in range(6):
        TeamY.append(pool.pop(rand(len(pool))))
    for x in range(6):
        TeamO.append(pool.pop(rand(len(pool))))

    return TeamY, TeamO


def load_team(path="../documents/pokemon.txt"):
    pp = parse_pokemon
    return pp(path)
