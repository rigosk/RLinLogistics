import numpy as np
import pandas as pd

class Agent(object):
    #Intialize
    def __init__(self,environment,random_factor=0):
        self.Q= {} #Qtable state-value
        self.init_reward(environment)
        self.random_factor=random_factor
        
        pass
    
    #Print Q value of all states    
    def print_Q(self):
        print(self.Q)
    
    #def init_reward(self, states):
        #for state in states:
            #self.Q[tuple(state)] = np.random.uniform(low=1.0, high=0.1)

    #Generate intial Q-values for each state-action pair combination    
    def init_reward(self, env):
        actions = env.all_actions
        states = env.all_states
        self.Q = pd.DataFrame(index = actions , columns = states)
        for state in range(len(states)):
            for action in range(len(actions)):
                self.Q[states[state]][actions[action]] = np.random.uniform(low=1.0, high=0.1)
        Qtable = self.Q
        print("\n QTable:")
        print(Qtable)

    #Action: assign case to judge
    #To do: 
    def assign_case_to_judge(self,env,state,case,available_actions):
        print("In this state the available actions are",available_actions)
        
        BestAction = []
        if available_actions == []:
            done =  1
            BestAction = None
            return BestAction,done

        n = np.random.random()
        current_state = state
        
        #To do: make discount and alpha in input value
        Discount = 1
        alpha = 0.5
        done = 0
        RTable = {}
        print('\n current state: ', current_state)
        #Determine action - Exploration vs Explotation tradeoff
        if n < self.random_factor:
            index = np.random.random_integers(0,len(available_actions))
            BestAction = available_actions[index]
            RTable[BestAction] = env.give_reward(current_state, BestAction, case)
        else:
            
            #Step 2b: choose action with highest reward
            RTable = dict.fromkeys(available_actions) 
            for a in range(len(available_actions)):
                #reward = env.give_reward(self, state, action, case) states contains workload and availability, action contains assignemnt to judge, case contains hours. 
                RTable[available_actions[a]] = env.give_reward(current_state, available_actions[a], case)
            BestAction = env.keywithminval(RTable)
            print('BestAction: ',BestAction)
            
        #Step 2b: Determine Max Q value from PrevIteration
        new_state = env.new_state(BestAction)
        if new_state == 999:
            done =  1
            BestAction = None
            return BestAction,done
        
        MaxPrevIteration = self.Q[tuple(new_state)].max()
        print('new state: ', new_state)
        #Step 2b: Calculate q-value: direct reward + highest q value for state-action pair for new state in previous iteration
        q_value = (Discount * MaxPrevIteration) + RTable[BestAction]
        print('\n q_value [', q_value, '] = ', Discount * MaxPrevIteration,'+', RTable[BestAction])
        
        #Step 2c: update value function, can stay none>> so no improvement or no actions left in available actions
        UpdatedQ = (1-alpha)*self.Q[tuple(current_state)][BestAction] + alpha*q_value
        print('\n UpdatedQ [', UpdatedQ, '] = ', (1-alpha), '*', self.Q[tuple(current_state)][BestAction],'+', alpha,'*',q_value)
        self.Q[tuple(current_state)][BestAction] = UpdatedQ
        
            
            #for action in available_actions:  
            #current_state = state
            #new_state = tuple(available_actions[action])
            #print("\tValue of vailable state", new_state," is ",self.Q[new_state])
            #To do: add stepwise q-learning function
            # if self.Q[action][current_state] >= maxG:
            #reward = ...env.give_reward(self,judge,case)
            #reward = ...env.give_reward(self, state, action,case) states contains workload and availability, action contains assignemnt to judge, case contains hours. 
                #Update Q value function: previous state-action q value + new state-action q value
                #if self.Q[action][current_state] >= maxG:
                    #print('value', self.Q[new_state])
                    #next_move = action
                    #maxG = self.Q[new_state]
                    # print("Highest value is ",maxG, "so action ", next_move, " is selected")
        return BestAction,done
