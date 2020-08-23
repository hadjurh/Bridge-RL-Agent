# Bridge-RL-Agent

Hugo Hadjur - Ishii Lab - 10/2017 to 09/2018

## How to use the current version

(Developed and tested with Python 3.6.3)

### Generate games

`python3 generate.py arg1 arg2 arg3` or
run `scripts/generate.sh arg1 arg2 arg3`

* `arg1`: Total number of generated games

* `arg2`: Number of games per file

* `arg3`: Unique ID (in case of running two programs that create
two exact same file names)

### Learn from database

Q-Learning: `python3 qlearning_learn.py arg1 arg2` or
run `scripts/qlearning_learn.sh arg1 arg2`

SARSA: `python3 sarsa_learn.py arg1 arg2` or
run `scripts/sarsa_learn.sh arg1 arg2`

* `arg1`: Which `.game` files to learn from
(example for all files: `*.game`)

* `arg2`: Unique ID

### (Optional) Combine knowledge

`python3 merge_dictionaries.py arg1 arg2` or
run `scripts/merge.sh arg1 arg2`

* `arg1`: Which `.json` files to combine.
Have to specify Q-Learning or SARSA folder.
Example: `arg1` = `sarsa/*.json` or `qlearning/*.json`

* `arg2`: Unique ID

### Let an agent play

`python3 agent_play.py arg1 arg2 arg3` or
run `scripts/brain_test.sh arg1 arg2 arg3`

* `arg1`: Which `.json` files to play with
(example for all files from qlearning folder:
`arg1` = `qlearning/*.json`)

* `arg2`: Number of games

* `arg3`: Number of samples

Total number of tested games per `.json` file: `arg2` * `arg3`

## DQN (primitive form)

Use `python3 dqn_learn.py arg1 arg2`

* `arg1`: Which `.game` files to learn from
(example for all files: `*.game`)

* `arg2`: Unique ID

And `python3 dqn_play.py arg1 arg2 arg3`

* `arg1`: memory file

* `arg2`: Number of games

* `arg3`: Number of samples

## TODOs

* Implement trump play/trump learning

* Learn as defender (make a heuristic strategy for attackers)

* Train trained declarer against trained defender
(double agent training)

* Try negative learning
(keep losing examples to add negative rewards)

* Implement DQN so that it gives better results
