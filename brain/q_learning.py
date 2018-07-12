from game.cards import Card, observation_to_card


class RL:
    def __init__(self, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9, memory=None):
        self.actions = []  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        if memory is None:
            self.q_table = dict()
        else:
            self.q_table = memory

    def check_state_exist(self, state):
        if str(state) not in list(self.q_table.keys()):
            # Append new state to q table
            self.q_table[str(state)] = dict()


# off-policy
class QLearningTable(RL):
    def __init__(self, learning_rate=0.1, reward_decay=0.9, e_greedy=0.9, memory=None):
        super(QLearningTable, self).__init__(learning_rate, reward_decay, e_greedy, memory)

    def learn(self, s, a, s_, r, close_cards_learning=True, distance=0):
        gamma_close_states = 0.8

        self.check_state_exist(s_)
        self.check_state_exist(s)

        current_value = self.q_table[str(s)][str(a)] if a in self.q_table[str(s)].keys() else 0
        estimate_optimal = 0 if list(self.q_table[str(s_)].keys()) == [] else max(self.q_table[str(s_)].values())

        learned_value = r * (gamma_close_states ** distance) + self.gamma * estimate_optimal
        self.q_table[str(s)][str(a)] = (1 - self.lr) * current_value + self.lr * learned_value  # update

        if close_cards_learning:
            close_cards = observation_to_card(a).close_cards()
            for distance in [1, 2, 3]:
                for card in close_cards[distance]:
                    self.learn(s, card.observation(), s_, r, close_cards_learning=False, distance=distance)
