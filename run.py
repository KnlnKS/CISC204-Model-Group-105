# Python Libraries
import math
import pickle
import os
from random import randrange as rand

# CISC 204 Libraries
from nnf import Var
from lib204 import Encoding

# Project Libraries
from helper_functions.team_gen import load_team
from helper_functions.team_gen import team_gen as tg
from helper_functions.least_x_of_y import least_two_of_six as l2o6
from helper_functions.least_x_of_y import least_four_of_six as l4o6
from helper_functions.api_methods import calc, get_move_info, get_attacker, get_defender
from helper_functions.type_resist import weak_to

"""
https://www.smogon.com/dex/sm/formats/ou/
"""

team_vars = []


def mega_evolve(pokemon):
    if pokemon['item'][-3:] == 'ite':
        pokemon['name'] = pokemon['name'] + '-Mega'

    return pokemon


def rand_var(multi, sets=[1, 1, 2], val=None):
    x = 100000000

    if multi == sets[0]:
        return Var(str(rand(x))) | Var(str(rand(x)))  # 75%
    elif multi > sets[2]:
        return Var(str(rand(x))) & Var(str(rand(x)))  # 25%

    return val  # 50%


def theory(yt, ot):
    E = Encoding()
    for opoke in range(len(ot)):
        temp_vars = []
        for ypoke in range(len(yt)):
            if yt[ypoke]['strategy'] == 'Wall Breaker':
                # Formula variables
                matchup = 0  # Final variable representing final formula
                outspeed = Var(yt[ypoke]['name'] + ' outspeeds ' + ot[opoke]['name'])  # Is your Pokemon faster
                resist = Var(yt[ypoke]['name'] + ' resists ' + ot[opoke]['name'])  # Does your Pokemon resist
                rand_dmg_mod = Var(yt[ypoke]['name'] + ' rolls high damage')  # Random damage modifier
                pred_damage = Var(yt[ypoke]['name'] + ' deals high damage')  # Pokemon damage
                low_pred_damage = Var(yt[ypoke]['name'] + ' deals low damage')  # Pokemon damage

                # Get types, hp, and speed
                calc(yt[ypoke], ot[opoke], {'name': 'Tail Whip'})
                attacker_state = {
                    'types': get_attacker()['types'],
                    'hp': get_attacker()['stats']['hp'],
                    'spe': get_attacker()['stats']['spe']
                }
                defender_state = {
                    'types': get_defender()['types'],
                    'hp': get_defender()['stats']['hp'],
                    'spe': get_defender()['stats']['spe']
                }

                # Get type match multipliers
                def_pred_multi = weak_to(attacker_state['types'], defender_state['types'])
                if not (def_pred_multi < 1):
                    resist = rand_var(def_pred_multi, val=resist)
                else:
                    E.add_constraint(resist)

                # Check if Pokemon outspeeds opponent
                if attacker_state['spe'] > defender_state['spe']:
                    E.add_constraint(outspeed)
                elif attacker_state['spe'] < defender_state['spe']:
                    E.add_constraint(~outspeed)

                attacker_best_move = [-9999]

                for m in yt[ypoke]['moves']:
                    if get_move_info({'name': m})['category'] != 'Status':
                        damage = calc(yt[ypoke], ot[opoke], {'name': m})['damage']
                        if damage != 0 and damage[0] > attacker_best_move[0]:
                            attacker_best_move = damage

                pred_turns = math.ceil(defender_state['hp'] / attacker_best_move[-1])
                pred_turns_low = math.ceil(defender_state['hp'] / attacker_best_move[0])

                if pred_turns == 1:
                    E.add_constraint(rand_dmg_mod)
                    E.add_constraint(pred_damage)
                    temp_vars.append((rand_dmg_mod & pred_damage) & (outspeed | resist))
                elif pred_turns == pred_turns_low:
                    E.add_constraint(rand_dmg_mod)
                    pred_damage = rand_var(pred_turns, sets=[2, 3, 2], val=pred_damage)
                    temp_vars.append((rand_dmg_mod & pred_damage) & (outspeed | resist))
                else:
                    pred_damage = rand_var(pred_turns, sets=[2, 3, 2], val=pred_damage)
                    low_pred_damage = rand_var(pred_turns_low, sets=[2, 3, 2], val=low_pred_damage)
                    temp_vars.append(
                        ((rand_dmg_mod & pred_damage) | (~rand_dmg_mod & low_pred_damage)) & (outspeed | resist))

            elif yt[ypoke]['strategy'] == 'Wall':
                # Formula variables
                matchup = 0  # Final variable representing final formula
                resist = Var(yt[ypoke]['name'] + ' resists ' + ot[opoke]['name'])  # Does your Pokemon resist
                rand_dmg_mod = Var(yt[ypoke]['name'] + ' rolls high damage')  # Random damage modifier
                pred_damage = Var(ot[opoke]['name'] + ' deals high damage')  # Opponent's Pokemon damage
                low_pred_damage = Var(ot[opoke]['name'] + ' deals low damage')  # Opponent's Pokemon damage
                status_moves = Var(yt[ypoke]['name'] + ' has status move')  # Pokemon has status moves

                # Get types, hp, and speed
                calc(yt[ypoke], ot[opoke], {'name': 'Tail Whip'})
                attacker_state = {
                    'types': get_attacker()['types'],
                    'hp': get_attacker()['stats']['hp'],
                    'spe': get_attacker()['stats']['spe']
                }
                defender_state = {
                    'types': get_defender()['types'],
                    'hp': get_defender()['stats']['hp'],
                    'spe': get_defender()['stats']['spe']
                }

                # Get type match multipliers
                def_pred_multi = weak_to(attacker_state['types'], defender_state['types'])
                if not (def_pred_multi < 1):
                    resist = rand_var(def_pred_multi, val=resist)
                else:
                    E.add_constraint(resist)

                defender_best_move = [-9999]

                for m in ot[opoke]['moves']:
                    if get_move_info({'name': m})['category'] != 'Status':
                        damage = calc(ot[opoke], yt[ypoke], {'name': m})['damage']
                        if type(damage) is list and damage[0] > defender_best_move[0]:
                            defender_best_move = damage

                status = 0
                for m in yt[ypoke]['moves']:
                    if get_move_info({'name': m})['category'] == 'Status':
                        status += 1

                if status >= 2:
                    E.add_constraint(status_moves)
                else:
                    E.add_constraint(~status_moves)

                pred_turns = math.ceil(attacker_state['hp'] / defender_best_move[-1])
                pred_turns_low = math.ceil(attacker_state['hp'] / defender_best_move[0])

                if pred_turns == 1:
                    E.add_constraint(rand_dmg_mod)
                    E.add_constraint(pred_damage)
                    temp_vars.append((rand_dmg_mod & pred_damage).negate() & (status_moves | resist))
                elif pred_turns == pred_turns_low:
                    E.add_constraint(rand_dmg_mod)
                    pred_damage = rand_var(pred_turns, sets=[2, 3, 2], val=pred_damage)
                    temp_vars.append((rand_dmg_mod & pred_damage).negate() & (status_moves | resist))
                else:
                    pred_damage = rand_var(pred_turns, sets=[2, 3, 2], val=pred_damage)
                    low_pred_damage = rand_var(pred_turns_low, sets=[2, 3, 2], val=low_pred_damage)
                    temp_vars.append(
                        ((rand_dmg_mod & pred_damage) | (~rand_dmg_mod & low_pred_damage)).negate() & (
                                status_moves | resist))

            elif yt[ypoke]['strategy'] == 'Sweeper':
                # Formula variables
                matchup = 0  # Final variable representing final formula
                resist = Var(yt[ypoke]['name'] + ' resists ' + ot[opoke]['name'])  # Does your Pokemon resist
                rand_dmg_mod = Var(yt[ypoke]['name'] + ' rolls high damage')  # Random damage modifier
                pred_damage = Var(ot[opoke]['name'] + ' deals high damage')  # Opponent's Pokemon damage
                low_pred_damage = Var(ot[opoke]['name'] + ' deals low damage')  # Opponent's Pokemon damage

                # Get types, hp, and speed
                calc(yt[ypoke], ot[opoke], {'name': 'Tail Whip'})
                attacker_state = {
                    'types': get_attacker()['types'],
                    'hp': get_attacker()['stats']['hp'],
                    'spe': get_attacker()['stats']['spe']
                }
                defender_state = {
                    'types': get_defender()['types'],
                    'hp': get_defender()['stats']['hp'],
                    'spe': get_defender()['stats']['spe']
                }

                # Get type match multipliers
                def_pred_multi = weak_to(attacker_state['types'], defender_state['types'])
                if not (def_pred_multi < 1):
                    resist = rand_var(def_pred_multi, val=resist)
                else:
                    E.add_constraint(resist)

                attacker_best_move = [-9999]

                for m in yt[ypoke]['moves']:
                    if get_move_info({'name': m})['category'] != 'Status':
                        damage = calc(yt[ypoke], ot[opoke], {'name': m})['damage']
                        if damage != 0 and damage[0] > attacker_best_move[0]:
                            attacker_best_move = damage

                pred_turns = math.ceil(defender_state['hp'] / attacker_best_move[-1] * 1.5)
                pred_turns_low = math.ceil(defender_state['hp'] / attacker_best_move[0] * 1.5)

                if pred_turns == 1:
                    E.add_constraint(rand_dmg_mod)
                    E.add_constraint(pred_damage)
                    temp_vars.append((rand_dmg_mod & pred_damage) & resist)
                elif pred_turns == pred_turns_low:
                    E.add_constraint(rand_dmg_mod)
                    pred_damage = rand_var(pred_turns, sets=[2, 3, 2], val=pred_damage)
                    temp_vars.append((rand_dmg_mod & pred_damage) & resist)
                else:
                    pred_damage = rand_var(pred_turns, sets=[2, 3, 2], val=pred_damage)
                    low_pred_damage = rand_var(pred_turns_low, sets=[2, 3, 2], val=low_pred_damage)
                    temp_vars.append(
                        ((rand_dmg_mod & pred_damage) | (~rand_dmg_mod & low_pred_damage)) & resist)

        team_vars.append(l2o6(temp_vars[0], temp_vars[1], temp_vars[2], temp_vars[3], temp_vars[4], temp_vars[5]))

        print(ot[opoke]['name'] + "'s theory has been formulated!")

    E.add_constraint(team_vars[0] | team_vars[1] | team_vars[2] | team_vars[3] | team_vars[4] | team_vars[5])
    return E


if __name__ == "__main__":
    # Acts as a test of model
    choice = 0
    y, o = tg("documents/pokemon.txt")

    print('Hi, welcome to the Pokemon Battle Estimator!')
    while choice <1 or choice >5:
        print('Please choose from the following options.')
        print('1. Choose random Pokemon to face each other!')
        print('2. See how you fair with a team of strong Pokemon against weak ones!')
        print('3. See how you fair with a team of weak Pokemon against strong ones!')
        print('4. See how you fair with a team of your choosing against a strong one!')
        print('5. See how you fair with a team of your choosing against a weak one!')
        choice = int(input())
        print()

    if choice == 2:
        y = load_team("documents/teams/strong_team.txt")
        o = load_team("documents/teams/weak_team.txt")
    elif choice == 3:
        o = load_team("documents/teams/strong_team.txt")
        y = load_team("documents/teams/weak_team.txt")
    elif choice == 4:
        y = load_team("documents/teams/custom_team.txt")
        o = load_team("documents/teams/strong_team.txt")
    elif choice == 5:
        y = load_team("documents/teams/custom_team.txt")
        o = load_team("documents/teams/weak_team.txt")

    print("Your team consists of:")
    for p in y:
        print(p['name'])
    print("\nYour opponent's team consists of:")
    for p in o:
        print(p['name'])
    print("\nCreating Theory...")

    T = theory(y, o)

    with open("classes/theory.pyclass", 'wb+') as output:  # Overwrites any existing file.
        pickle.dump(T, output, -1)

    with open("classes/team.pyclass", 'wb+') as output:  # Overwrites any existing file.
        pickle.dump(team_vars, output, -1)

    with open("classes/pokemons.pyclass", 'wb+') as output:  # Overwrites any existing file.
        pickle.dump(o, output, -1)

    print('\nDoing theory stuff...')
    print()
    os.system("ubuntu run python3 theory.py")
