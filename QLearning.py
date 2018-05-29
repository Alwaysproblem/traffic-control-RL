import numpy as np
import pandas as pd
import random as rd

class QL:
    def __init__(self, actionSpace, epsilon, gamma, alpha):
        """
        please when using the learn function,
        don't forget initialize the state.
        """
        self.actionSpace = actionSpace
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.QTable = pd.DataFrame(columns = self.actionSpace, dtype = np.float)
        self.R = 0
        self.observation = None
        # self.Qtable = None
        # self.state = None
        # self.SList = []
        # self.policyList = []

    def reward(self, state):
        """ reward function, which should be get value from the in surroundings."""
        self.R = 0
        pass
        return self.R

    def updateValueQtable(self, cur_state, action, next_state, Next_action, reward):
        self.QTable.loc[cur_state, action] += self.alpha * (
                                            reward + \
                                            self.gamma * self.QTable.loc[next_state, Next_action] - \
                                            self.QTable.loc[cur_state, action]
                                        )

    def stateExist(self,state):
        """check the state if it already exits in the Q Table."""
        if state in self.QTable.index:
            return True
        else:
            return False

    def extendQtable(self, state):
        if not self.stateExist(state):
            self.QTable = self.QTable.append(
                pd.Series(
                    [0]*len(self.actionSpace),
                    index = self.QTable.columns,
                    name = state,
                )
            )

    def epsilonGreedy(self, state):
        """epsilon greedy algorithm."""
        self.extendQtable(state)
        if rd.random() < self.epsilon:
            action = self.BestPolicy(state)
        else:
            action = np.random.choice(self.actionSpace)
        return action

    def BestPolicy(self, state):
        """ take an action into the environment"""
        # if self.QTable.shape[0] == 0:
        #     return np.random.choice(self.actionSpace)
        # else:
        actions = self.QTable.loc[state, :]
        actions = actions.reindex(np.random.permutation(actions.index))
        return actions.idxmax()

    def initial_State(self, init_S):
        self.observation = init_S

    def learning(self, rewardfun = False, env_step = None):
        
        if self.observation == None:
            print("you should be intialize the self.state")
            return
        
        action = self.epsilonGreedy(str(self.observation))

        try:
            observation_, reward, done = env_step(int(action))
        except TypeError:
            print("there is no env.step(action).")

        if rewardfun is True:
            reward = self.reward(observation_)

        action_ = self.epsilonGreedy(str(observation_))

        self.updateValueQtable(str(self.observation), action, str(observation_), action_, reward)

        self.observation = observation_

        return done

    def acquireState(self, state):
        """acquire state from environment."""
        pass

    def takeAction(self, env):
        pass


if __name__ == "__main__":
    Q = QL(['u', 'd', 'l', 'r'], 0.9, 0.9, 0.5)
    # print(Q.BestPolicy(str([1, 2, 3, 4])))

    Q.extendQtable(str([1, 2, 3, 4]))
    Q.extendQtable(str([2, 4, 6, 5]))
    Q.extendQtable(str([1, 4, 5, 3]))
    Q.extendQtable(str([2, 9, 8, 7]))

    Q.QTable.loc[str([1, 2, 3, 4]), 'l'] = 2.3
    Q.QTable.loc[str([2, 4, 6, 5]), 'r'] = 2.4
    Q.QTable.loc[str([1, 4, 5, 3]), 'u'] = 2.5
    Q.QTable.loc[str([2, 9, 8, 7]), 'd'] = 2.6

    print(Q.QTable)
    # print(Q.BestPolicy(str([1, 2, 3, 4])))
    Q.updateValueQtable(
        str([1, 2, 3, 4]), 
        Q.BestPolicy(str([1, 2, 3, 4])), 
        str([2, 4, 6, 5]), 
        Q.BestPolicy(str([2, 4, 6, 5])),
        1
    )
    
    print(Q.QTable)

