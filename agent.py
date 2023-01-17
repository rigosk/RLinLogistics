import numpy as np

class Agent(object):
    def __init__(self,environment,random_factor=0.2):
        print("hi")
        self.Q= {} #Qtable state-value
        self.init_reward(environment.all_states)
        self.random_factor=random_factor



        pass

    def print_Q(self):
        print(self.Q)
    def init_reward(self, states):

        for state in states:
            self.Q[tuple(state)] = np.random.uniform(low=1.0, high=0.1)


    #ACTIONS
    def assign_case_to_judge(self,env,state,case,available_actions):
        print("In this state the available actions are",available_actions)

        maxG = -10e15
        judge_to_assign_case=None
        next_move=None
        n = np.random.random()
        if n < self.random_factor:
            next_move = np.random.choice(list(available_actions.keys()))
        else:
            for action in available_actions:

                new_state = tuple(available_actions[action])
                print("\tValue of vailable state", new_state," is ",self.Q[new_state])



                if self.Q[new_state] >= maxG:
                    #print('value', self.Q[new_state])
                    next_move = action
                    maxG = self.Q[new_state]


        print("Highest value is ",maxG, "so action ", next_move, " is selected")
        return next_move
