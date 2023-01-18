import numpy as np

class Agent(object):
    #Intialize
    def __init__(self,environment,random_factor=0.2):
        print("hi")
        self.Q= {} #Qtable state-value
        self.init_reward(environment.all_states)
        self.random_factor=random_factor

        pass
    
    #Print Q value of all states    
    def print_Q(self):
        print(self.Q)
    def init_reward(self, states):
        for state in states:
            self.Q[tuple(state)] = np.random.uniform(low=1.0, high=0.1)
    '''
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
         '''
         
    #Action: assign case to judge
    #To do: reward is not incorporated, function plan.give_reward not called
    def assign_case_to_judge(self,env,state,case,available_actions):
        print("In this state the available actions are",available_actions)

        maxG = -10e15
        judge_to_assign_case=None
        next_move=None
        n = np.random.random()
        if n < self.random_factor:
            next_move = np.random.choice(list(available_actions.keys()))
        else:
            
            #choose action whith highest reward
            for action in available_actions:

                new_state = tuple(available_actions[action])
                print("\tValue of vailable state", new_state," is ",self.Q[new_state])

                #Step 2b: update value function
                #To do: add stepwise q-learning function
                if self.Q[new_state] >= maxG:
                    #print('value', self.Q[new_state])
                    next_move = action
                    maxG = self.Q[new_state]


        print("Highest value is ",maxG, "so action ", next_move, " is selected")
        return next_move
