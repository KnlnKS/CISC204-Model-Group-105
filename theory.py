import pickle

# CISC 204 Libraries
from lib204 import Encoding

if __name__ == "__main__":
    # This is a default team. your_team is strong, while oppo_team is weak.
    # Acts as a test of model
    T = Encoding()
    team_vars = []
    pokemon_team = []

    with open('classes/theory.pyclass', 'rb') as input:
        T = pickle.load(input)

    with open('classes/team.pyclass', 'rb') as input:
        team_vars = pickle.load(input)

    with open('classes/pokemons.pyclass', 'rb') as input:
        pokemon_team = pickle.load(input)

    print("Possibility of Winning?: %s" % T.is_satisfiable())

    chance = (T.count_solutions(team_vars) / T.count_solutions())
    print("Estimated chance of winning:  %.2f" % chance)
    if chance < 0.6:
        print("You will probably lose.")
    elif chance < 0.7:
        print("It can go either way.")
    else:
        print("You will probably win!")
    print('Theory Size: %d' % T.size())

    worst = 1.0
    name = ''
    for v, vn in zip([team_vars[0], team_vars[1], team_vars[2], team_vars[3], team_vars[4], team_vars[5]],
                     pokemon_team):
        x = T.likelihood(v)
        if x < worst:
            worst = x
            name = vn['name']

    print("Pokemon to watch out for:     %s" % name)
