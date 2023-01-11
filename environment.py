from queue import Queue
import itertools

import numpy as np
import numpy.random as rand

#np.roll(x2, 1, axis=0)

class Env(object):
    def __init__(self, num_of_judges, size_of_queues, num_of_trial_classes):
        a = np.random.random(num_of_trial_classes)
        a /= a.sum()
        self.case_probability =a
            #rand.uniform(0, 1, size=num_of_trial_classes) #this is the probability of a new case to be of this class
        print('Probabilities for the arriving cases are: ')
        print('Class \t Probability')
        for i in range(len(self.case_probability)):
            print(i,"\t:",self.case_probability[i])

        self.size_of_queues = size_of_queues
        self.num_of_trial_classes = num_of_trial_classes

        self.num_of_judges = num_of_judges
        self.judges_specialities=self.set_specialities_of_judges()
        #np.random.choice(a=[0,1], size=(num_of_judges,num_of_trial_classes),p=[0.7, 0.3]) #p is the distribution, we can adjust accordingly
        self.all_states=self.all_possibilities()


        self.queues=[]
        for i in range(num_of_judges):
            self.queues.append(Queue(maxsize=size_of_queues))

        #the state is the indexes (size) of all queues
        self.state = [0] * num_of_judges



    def print_env(self):
        print("this is the print")
        for i in range(self.num_of_judges):
            print("Judge ",i)
            print(self.queues[i].queue)
            #for n in list(self.state[i].queue):
             #   print(n, end="s ")
        print(self.judges_specialities)

    def update_state(self,case,action):
        print("action",action)


        print('CASE', case)
        temp=[]
        self.queues[action].put(case)

        for i in range(len(self.queues)):
            print("lll", list(self.queues[i].queue))
            temp.append(self.queues[i].qsize())
            self.state=temp


    def construct_allowed_states(self,state):
        '''Creating the allowed states after the current state'''
        cand_states=[]
        allowed_states=[]
        allowed_moves={}
        for i in range(len(state)):

            if (state[i]<self.size_of_queues-1): # if a judge has not reach the limit of the queue
                cand_states.append(i)

        for st in cand_states:

            #allowed_states.append(state.copy())
            #allowed_states[-1][st]=allowed_states[-1][st]+1

            allowed_states=state.copy()
            allowed_states[st] = allowed_states[st] + 1
            allowed_moves[st]=allowed_states
            #print("from",state,"to",allowed_moves[st])




        return allowed_moves

    def all_possibilities(self):
        '''creates all possible states'''

        #if you want list to return
        #return (list(tup) for tup in itertools.combinations(range(self.size_of_queues),self.num_of_judges))

        #if you want tuples
        #return itertools.combinations(range(self.size_of_queues),self.num_of_judges)
        return itertools.product(range(self.size_of_queues),repeat=self.num_of_judges)



    #reward
    def give_reward(self,judge,case):
        #if at end give 0 reward
        # if not at end give -1 reward

        if case==self.judges_specialities[judge]:
            return 0
        else:
            return -1
    #Cases
    def new_case(self):
        return np.random.choice(a=np.arange(self.num_of_trial_classes), size=(1,1),p=self.case_probability)
    #Queues
    def add_in_queue(self,judge,case):
        self.queues[judge].put(case)

    # every day remove last case from queue
    def next_day(self):
        for i in range(self.num_of_judges):
            self.state[i].get()

    def get_judge_schedule_length(self,judge):
        return self.state[judge].qsize()
    #Judges
    def set_specialities_of_judges(self):
        while(1):
            total_sum=0
            spec=np.random.choice(a=[0, 1], size=(self.num_of_judges, self.num_of_trial_classes),
                         p=[0.7, 0.3])  # p is the distribution, we can adjust accordingly
            for i in range(len(spec[:,0])):
                if spec[i,:].sum()>0:
                    total_sum=total_sum+1
            if total_sum==self.num_of_judges:
                return spec

    def is_speciality_of_judge(self,judge,speciality):
        return self.judges_specialities[judge,speciality]

    def get_judge_specialities(self,judge):
        return self.judges_specialities[judge, :]