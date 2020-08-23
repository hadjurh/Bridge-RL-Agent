#  &clubs; &diams; &hearts; &spades; QLearning-Bridge (Master's Thesis) &spades; &hearts; &diams; &clubs;

## The game of Bridge and its variant: MiniBridge

Contract Bridge is a 2 vs. 2 card game (North-South vs. East-West).

Each player has 13 cards when the game starts and plays one card at each trick. 

![alt text][bridge]

[bridge]: https://i.imgur.com/PnDDVVo.png "Logo Title Text 2"

The rules are complex, [here](http://www.acbl.org/learn_page/how-to-play-bridge/ "American Contract Bridge League Website") are some explanations on how to play.

## Objectives

The goal of this project is to test reinforcement learning algorithms applied to Contract Bridge. 

## Steps

The plan is defined as follows:
* Develop the game features (cards, players, rules).
* Implement a first basic learning strategy: **Q-Learning**. This algorithm only takes in account the observable states of the game.
    * Apply this technique to a restricted case (fewer cards than the usual game and/or defined cards).
    * Apply it to a wider range of possibilities.
* Predict the unseen information of the game.
    * Add **SARSA and POMDP** to the Q-Learning strategy.
    * Add **Bayesian estimation** to the Q-Learning strategy.
    * Add **Internal-State Policy-Gradient Methods** for POMDPs.
    
## Progress - Features

| Step          | Advancement   |
| ------------- | :-------------: |
| Q-Learning | &#10003; |
| SARSA | &#10003;      |

## Options

| Options        | Features       |
| ------------- | -------------|
| `s`, `--show` | Display graphics of the results |
| `p`, `--print`| Display information of every game in the console |
