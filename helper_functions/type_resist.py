TYPES = {
    'Normal': 'nor',
    'Fire': 'fir',
    'Water': 'wat',
    'Electric': 'ele',
    'Grass': 'gra',
    'Ice': 'ice',
    'Fighting': 'fig',
    'Poison': 'poi',
    'Ground': 'gro',
    'Flying': 'fly',
    'Psychic': 'psy',
    'Bug': 'bug',
    'Rock': 'roc',
    'Ghost': 'gho',
    'Dragon': 'dra',
    'Dark': 'dar',
    'Steel': 'ste',
    'Fairy': 'fai',
}


def weak_to(type1, type2):
    for t in range(len(type1)):
        type1[t] = TYPES[type1[t]]
    for t in range(len(type2)):
        type2[t] = TYPES[type2[t]]

    multi = 1;

    for x in type2:
        multi *= move_effectiveness(x, type1)

    return multi


def move_effectiveness(move_type, opponent_type):
    atk_multiplier = 1

    if move_type == "nor":
        for x in opponent_type:
            if x in ["roc", "ste"]:
                atk_multiplier *= 0.5
            elif x == 'gho':
                return 0
    elif move_type == "fir":
        for x in opponent_type:
            if x in ["gra", "ice", "bug", "ste"]:
                atk_multiplier *= 2
            elif x in ["fir", "wat", "roc", "dra"]:
                atk_multiplier *= 0.5
    elif move_type == "wat":
        for x in opponent_type:
            if x in ["fir", "gro", "roc"]:
                atk_multiplier *= 2
            elif x in ["wat", "gra", "dra"]:
                atk_multiplier *= 0.5
    elif move_type == "ele":
        for x in opponent_type:
            if x in ["wat", "fly"]:
                atk_multiplier *= 2
            elif x in ["ele", "gra", "dra"]:
                atk_multiplier *= 0.5
            elif x == 'gro':
                return 0
    elif move_type == "gra":
        for x in opponent_type:
            if x in ["wat", "gro", "roc"]:
                atk_multiplier *= 2
            elif x in ["fir", "gra", "poi", "fly", "bug", "dra", "ste"]:
                atk_multiplier *= 0.5
    elif move_type == "ice":
        for x in opponent_type:
            if x in ["gra", "gro", "fly", "dra"]:
                atk_multiplier *= 2
            elif x in ["fir", "wat", "ice", "ste"]:
                atk_multiplier *= 0.5
    elif move_type == "fig":
        for x in opponent_type:
            if x in ["nor", "ice", "roc", "dar", "ste"]:
                atk_multiplier *= 2
            elif x in ["poi", "fly", "psy", "bug", "gho", "fai"]:
                atk_multiplier *= 0.5
    elif move_type == "poi":
        for x in opponent_type:
            if x in ["gra", "fai"]:
                atk_multiplier *= 2
            elif x in ["poi", "gro", "roc", "gho"]:
                atk_multiplier *= 0.5
            elif x == 'ste':
                return 0
    elif move_type == "gro":
        for x in opponent_type:
            if x in ["fir", "ele", "poi", "roc", "ste"]:
                atk_multiplier *= 2
            elif x in ["gra", "bug"]:
                atk_multiplier *= 0.5
            elif x == 'fly':
                return 0
    elif move_type == "fly":
        for x in opponent_type:
            if x in ["gra", "fig", "bug"]:
                atk_multiplier *= 2
            elif x in ["ele", "roc", "ste"]:
                atk_multiplier *= 0.5
    elif move_type == "psy":
        for x in opponent_type:
            if x in ["fig", "poi"]:
                atk_multiplier *= 2
            elif x in ["psy", "ste"]:
                atk_multiplier *= 0.5
            elif x == "dar":
                return 0
    elif move_type == "bug":
        for x in opponent_type:
            if x in ["gra", "psy", "dar"]:
                atk_multiplier *= 2
            elif x in ["bug", "fig", "poi", "fly", "gho", "ste", "fai"]:
                atk_multiplier *= 0.5
    elif move_type == "roc":
        for x in opponent_type:
            if x in ["fir", "ice", "fly", "bug"]:
                atk_multiplier *= 2
            elif x in ["fig", "gro", "dar"]:
                atk_multiplier *= 0.5
    elif move_type == "gho":
        for x in opponent_type:
            if x in ["psy", "gho"]:
                atk_multiplier *= 2
            elif x in ["dar"]:
                atk_multiplier *= 0.5
            elif x == "nor":
                return 0
    elif move_type == "dra":
        for x in opponent_type:
            if x == 'dra':
                atk_multiplier *= 2
            elif x in ["ste"]:
                atk_multiplier *= 0.5
            elif x == 'fai':
                return 0
    elif move_type == "dar":
        for x in opponent_type:
            if x in ["psy", "gho"]:
                atk_multiplier *= 2
            elif x in ['poi', "dar", "fai"]:
                atk_multiplier *= 0.5
    elif move_type == "ste":
        for x in opponent_type:
            if x in ["ice", "roc", "fai"]:
                atk_multiplier *= 2
            elif x in ["fir", "wat", "ele", "ste"]:
                atk_multiplier *= 0.5
    elif move_type == "fai":
        for x in opponent_type:
            if x in ["fig", "dra", "dar"]:
                atk_multiplier *= 2
            elif x in ["fir", "poi", "ste"]:
                atk_multiplier *= 0.5
    return atk_multiplier
