import numpy as np

class Agent(object):
    def __init__(self,environment):
        print("hi")
        self.G= {}
        self.init_reward(environment.all_states)

    def print_G(self):
        print(self.G)
    def init_reward(self, states):

        for state in states:
            self.G[tuple(state)] = np.random.uniform(low=1.0, high=0.1)


    #ACTIONS
    def assign_case_to_judge(self,state,case,available_actions):
        print("actions",available_actions)
        maxG = -10e15
        judge_to_assign_case=None
        for action in available_actions:

            new_state = tuple(available_actions[action])
            print("\tAvailable state", new_state)


            if self.G[new_state] >= maxG:
                print('value',self.G[new_state])
                next_move = action
                maxG = self.G[new_state]

        return next_move
