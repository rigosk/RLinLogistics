import numpy as np
import tabulate as tb

class Agent(object):
    
    #Intialize
    def __init__(self,environment):
        self.QTable= {} #Empty dictionary, labeled list
        self.init_reward(environment.all_states,environment.all_actions)
        
    #Generate intial Q-values for each state-action pair combination    
    def init_reward(self, states,actions):
        states = list(states)
        i=0
        self.QTable[1,0]= "States"
        self.QTable[2,0]= "Actions"
        self.QTable[3,0]= "Qvalue"
        for state in range(len(states)):
           for a in range(len(actions)):
               i+=1
               self.QTable[1,i]=states[state]
               self.QTable[2,i]=actions[a]
               self.QTable[3,i] = np.random.uniform(low=1.0, high=0.1)
        Qtable = self.QTable
        #tb.tabulate(Qtable.
        
    #Print Q value of all states      
    def print_QTable(self):
        print(self.QTable)

    #Action: assign case to judge
    #To do: reward is not incorporated, function plan.give_reward not called
    def assign_case_to_judge(self,state,case,available_actions):
        print("available actions",available_actions)
        maxG = -10e15
        judge_to_assign_case=None
        
        #choose action whith highest reward
        for action in available_actions:
            new_state = tuple(available_actions[action])
            print("\tAvailable state", new_state)
            
            #Step 2b: update value function
            #To do: add stepwise q-learning function
            if self.QTable[new_state] >= maxG:
                print('value',self.QTable[new_state])
                next_move = action
                maxG = self.QTable[new_state]

        return next_move
