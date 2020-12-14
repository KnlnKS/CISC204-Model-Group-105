[![Work in Repl.it](https://classroom.github.com/assets/work-in-replit-14baed9a392b3a25080506f3b7b6d57f295ec2978f6f33ec97e36a161684cbe9.svg)](https://classroom.github.com/online_ide?assignment_repo_id=309543&assignment_repo_type=GroupAssignmentRepo)

# CISC/CMPE 204 Modelling Project

Welcome to the major project for CISC/CMPE 204 (Fall 2020)!

This project- named “GOTTA CATCH ‘EM ALL” aims to determine an estimate of how likely your team of Pokémon will beat another in battle. It will also return the Opponent's strongest Pokemon (in relation to your team). Before running the Python program, first run the api using `node index.js` when in the `pokemon-data/` folder.

## Requirements
* Node.js and NPM/Yarn
  * Needed as database/damage calculator is only available as a npm package
* Ubuntu as OS or WSL
  * Error with requirements library run running on windows.
  * Note: This branch is run of 2 ways to run the program. Try the other if this one doesn't work

## Structure

* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
* `documents/teams`: Folders containing Pokemon Team Data. There is markdown located there explaining how to make custom teams.
* `helper_functions`: Folder containing multiple methods used for the project including:
  * `api_methods.py`: Script to pull data from node/express app.
  * `least_x_of_y.py`: Script that creates formulas that evaluate to true when at least x of y total predicates are true.
  * `type_resist.py`: Script that checks if your type resists the opponent's, or if not how weak you are to them.
  * `team_gen.py`: Script that parses Smogon Pokemon Data into format usable by program.
* `pokemon-data`: Folder containing node/express app.
* `run.py`: General wrapper script that you can choose to use or not. Only requirement is that you implement the one function inside of there for the auto-checks.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.

