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
        if state not in list(self.q_table.keys()):
            # Append new state to q table
            self.q_table[state] = None


# off-policy
class QLearningTable(RL):
    def __init__(self, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9, memory=None):
        super(QLearningTable, self).__init__(learning_rate, reward_decay, e_greedy, memory)

    def learn(self, s, a, s_, r):
        self.check_state_exist(s_)
        self.check_state_exist(s)
        current_value = self.q_table[s][a]

        q_target = r + self.gamma * max(self.q_table[s_])
        self.q_table.ix[s, a] += (1 - self.lr) * q_predict + self.lr * q_target  # update
