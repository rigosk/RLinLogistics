from queue import Queue
import itertools

import numpy as np
import numpy.random as rand

class Env(object):
    
    #initialization of the object Env.
    def __init__(self, num_of_judges, size_of_queues, num_of_trial_classes, max_arrivals):
        
        #Calculate arrival probabilities for each case class
        a = np.random.random(num_of_trial_classes) # Generates an array a with random value's between 0-1, with a length of num_of_trail_classes. Each 
        a /= a.sum() # reseizes the values in the array to random values that has a total sum of 1. 
        self.case_probability =a
        
        #Print arrival probability of each class  
        #To Do: print values only from main file, so displace code to main script
        print('Probabilities for the arriving cases are: ')
        print('Class \t Probability')
        for i in range(len(self.case_probability)):
            print(i,"\t:",self.case_probability[i])
            
        #Generate environment, returns integers
        self.size_of_queues = size_of_queues
        self.num_of_trial_classes = num_of_trial_classes
        self.num_of_judges = num_of_judges
        self.max_arrivals = max_arrivals
        
        #Set specialities per judge, returns matrix
        self.judges_specialities=self.set_specialities_of_judges()
        self.all_states=self.all_possibilities()
        self.all_actions=self.gen_actions()

        #Creates a list in wich for each judge a queue object with a maximum length is generated. Special function uses, Queue
        self.queues=[]
        for i in range(num_of_judges):
            self.queues.append(Queue(maxsize=size_of_queues))

        #Initialize the state: [0,0,0], no cases in the judges queue's
        self.state = [0] * num_of_judges

    #Print information about judges and current queue length when called and ethe specialties of the judges.
    def print_env(self):
        print("this is the print")
        for i in range(self.num_of_judges):
            print("Judge ",i)
            print(self.queues[i].queue)
            #for n in list(self.state[i].queue):
             #   print(n, end="s ")
        print(self.judges_specialities)
    
    # state of the env object based on the case and the action (action is given by scheduler)
    def update_state(self,case,action):
        print("action",action)
        print('CASE', case)
        temp=[]
        self.queues[action].put(case)

        for i in range(len(self.queues)):
            print("lll", list(self.queues[i].queue))
            temp.append(self.queues[i].qsize())
            self.state=temp
    
    # Create possible next states and therefore actions.
    # To Do: Incorporate the specialty, is not done yet.         
    def construct_allowed_states(self,state):
        '''Creating the allowed states after the current state'''
        cand_states=[]
        allowed_states=[]
        allowed_moves={}
        
        # if a judge has not reach the limit of the queue, this is an candidate state that might change
        for i in range(len(state)):
            if (state[i]<self.size_of_queues-1): 
                cand_states.append(i)

        for st in cand_states:

            #allowed_states.append(state.copy())
            #allowed_states[-1][st]=allowed_states[-1][st]+1

            allowed_states=state.copy()
            allowed_states[st] = allowed_states[st] + 1
            allowed_moves[st]=allowed_states
            #print("from",state,"to",allowed_moves[st])
        return allowed_moves
    
    #Generates all possible states, state is number of cases in queue for each judge
    #To do: Change state from queue to schedule with blocks, all possible states when making an assignment choice depends on the possible allocations and availability of the judges
    def all_possibilities(self):
        '''creates all possible state-actionpairs'''

        #if you want list to return (changable)
        #return (list(tup) for tup in itertools.combinations(range(self.size_of_queues),self.num_of_judges))

        #if you want tuples (unchangable)
        #return itertools.combinations(range(self.size_of_queues),self.num_of_judges)
        return itertools.product(range(self.size_of_queues),repeat=self.num_of_judges)
    
    #Generate all possible actions. 
    #At each decision epoch the arrived cased must be assigned to a judge
    def gen_actions(self): 
        actions = []
        #"""
        prod = itertools.product(range(self.max_arrivals+1),repeat = self.num_of_judges)
        actions = list(prod)
        print("Generated Actions", actions)
        i=0    
        while i < len(actions):
            if not sum(actions[i])== self.max_arrivals:
                del actions[i]
                i-= 1
            i+=1
        print("Possible Actions", actions)
        return actions     
        #""" 

    #Calculate direct reward C(St,Xt)
    #To do: base reward on deviation from average workload over the judges and deviation from preferred due date. 
    def give_reward(self,judge,case):
        #if judge has specialty than 0 costs
        #if judge hasn't the specialty then 1 costs

        if case==self.judges_specialities[judge]:
            return 0
        else:
            return -1
        
    #Step 1: Generate new case, determines transition to new state. Corresponds with sample path Wn
    def new_case(self):
        return np.random.choice(a=np.arange(self.num_of_trial_classes), size=(1,1),p=self.case_probability)
    
    #Step 2c: Add case to chose queue
    #To do: Change queue to a schedule with availability blocks 
    def add_in_queue(self,judge,case):
        self.queues[judge].put(case)

    #Every day remove last case from queue
    #Delete when schedule with availability blocks is used in algorithm. Removing cases is not necessary, because time element is included. 
    def next_day(self):
        for i in range(self.num_of_judges):
            self.state[i].get()

    def get_judge_schedule_length(self,judge):
        return self.state[judge].qsize()
    
    #Step initialize Env: Set specialities per judge, each specialty must be assigned at least ones.
    #Function returns a matrix with 1 and 0
    #To do: verify is changing the indices doesn't corrupt the program (e.g. assigning the cases to judges)
    def set_specialities_of_judges(self):
        while(1):
            total_sum=0
            #If judge j can handle case i than 1, otherwise 0
            spec=np.random.choice(a=[0, 1], size=(self.num_of_judges, self.num_of_trial_classes),p=[0.7, 0.3])  # Random choosing between 0 and 1 based on p (the distribution), we can adjust accordingly
            for i in range(len(spec[0,:])):
                if spec[:,i].sum()>0:
                    total_sum=total_sum+1
                if total_sum==self.num_of_trial_classes: #Each speciality is assigned at least ones. 
                    return spec
                
    #Returns true if judge j has specialty i
    def is_speciality_of_judge(self,judge,speciality):
        return self.judges_specialities[judge,speciality]
    
    #Returns array with all specialties of judge j
    def get_judge_specialities(self,judge):
        return self.judges_specialities[judge, :]