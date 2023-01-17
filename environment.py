from queue import Queue
import itertools
#import pandas as pd
import numpy as np
import numpy.random as rand

#np.roll(x2, 1, axis=0)

class environment(object):
    def __init__(self, num_of_judges, days_to_schedule, num_of_case_classes,max_hours_for_case):
        self.num_of_judges = num_of_judges
        self.days_to_schedule = days_to_schedule
        self.num_of_case_classes = num_of_case_classes
        self.max_hours_for_case = max_hours_for_case


        self.case_probability =self.init_case_classes_probability(num_of_case_classes) #probability that a new case is of that class
        self.hours_probability=self.init_case_hours_probability(max_hours_for_case) #probability of hours needed for a new case

        self.available_judges=np.arange(num_of_judges) #if days of scheduled has exceeded for a judge then hebecomes not available anymore for scheduling
        self.judges_specialities=self.set_specialities_of_judges()
        self.judges_availability=self.init_judges_availability()
        self.all_states=self.all_possibilities()

        #self.action_space=[*range(num_of_judges)] #judge where the case will be assigned to
        self.action_space=action_space(num_of_judges)
        self.observation_space=list(np.zeros(num_of_judges, dtype=int))#,self.judges_availability[:,0],0]#hours per judge? + the case class
        self.case=self.new_case()


        self.schedule=[]
        self.queues=[]
        for i in range(num_of_judges):
            self.queues.append(Queue(maxsize=days_to_schedule))






    def step(self,action):
        done=0

        if action==None:
            done=1
        else:

            if self.observation_space[action]==self.days_to_schedule:
                self.observation_space[action] = 999
            else:
                self.observation_space[action]+=1
        #check if judge is available on that day



#        self.observation_space[action] = self.observation_space[action] + 1
        reward=1#self.give_reward(action,self.case)

        #check whether we have finished
       # counter=0
        #for judge in range(self.num_of_judges):

        #    if self.observation_space[judge]==self.days_to_schedule:
         #      counter=counter+1
        #if counter==self.num_of_judges:
         #   done=1

        return   reward, done

    def available_state(self):
        '''returns the day that each judge is available after non-availability dates'''
        for judge in range(self.num_of_judges):
            if self.judges_availability[judge][self.observation_space[judge]]==0:
                self.observation_space[judge]=self.observation_space[judge]+1

    def reset(self):
        '''reset the environment'''
        self.__init__(self.num_of_judges, self.days_to_schedule, self.num_of_case_classes,self.max_hours_for_case)

    def init_case_classes_probability(self,num_of_case_classes):
        '''initialize for the given number of case classes the probability that the may show when simulating '''
        a = np.random.random(num_of_case_classes)  # initialize random numbers for each trial class
        a /= a.sum()  # normalize
        return a

    def init_case_hours_probability(self,max_hours_for_case):
        h = np.random.random(max_hours_for_case)  # initialize random numbers for each trial class
        h /= h.sum()  # normalize
        return h

    def init_judges_availability(self):
        return np.random.choice(a=[0, 1], size=(self.num_of_judges, self.days_to_schedule),p=[0.3, 0.7])  # p is the distribution, we can adjust accordingly

    def print_case_classes_probability(self):
        print('Probabilities for the arriving cases are: ')
        print('Class \t Probability')
        for i in range(len(self.case_probability)):
            print(i, "\t:", self.case_probability[i])

    def print_case_hours_probability(self):
        print('Probabilities for the hours per case: ')
        print('hours \t Probability')
        for i in range(len(self.hours_probability)):
            print(i+1, "\t:", self.hours_probability[i])

    def print_env(self):
        self.print_case_classes_probability()
        self.print_case_hours_probability()
        print("self.observation_space", self.observation_space)
        print("self.judges_availability \n",self.judges_availability)
        print("Action Space:")
        print(self.action_space)
        print("judges specialities")
        print(self.judges_specialities)

    def update_state(self,case,action):

        temp=[]
        self.queues[action].put(case)

        for i in range(len(self.queues)):
            print("lll", list(self.queues[i].queue))
            temp.append(self.queues[i].qsize())
            self.observation_space=temp


    def construct_allowed_states(self,state):
        '''Creating the allowed states after the current state'''
        cand_states=[]
        allowed_states=[]
        allowed_moves={}
        for i in range(len(self.observation_space)):
            while ((self.observation_space[i] < self.days_to_schedule )and (self.judges_availability[i][self.observation_space[i]] == 0)):
                self.observation_space[i] += 1



            if (self.observation_space[i]<self.days_to_schedule)and (self.judges_availability[i][self.observation_space[i]]>0): # if a judge has not reach the limit of the queue
                #print("lalala", self.judges_availability, i, state[i])
                cand_states.append(i)


        for st in cand_states:

            #allowed_states.append(state.copy())
            #allowed_states[-1][st]=allowed_states[-1][st]+1

            allowed_states=self.observation_space.copy()
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
        return itertools.product(range(self.days_to_schedule+1), repeat=self.num_of_judges)

    def all_possible_states(self):
        mylist=[]
        for judge in range(self.num_of_judges):
            index=0
            a=[]
            for available_day in self.judges_availability[judge]:
                if available_day==1:
                    a.append(index)
                index=index+1

            mylist.append(a)
        print("judge", judge, "availability", list(mylist))
        reshape_factor=2
        ab=np.array(np.meshgrid(*mylist)).T.reshape(-1,self.num_of_judges) #gives all possible combinations of the arrays in mylist
        print(ab)






    #reward
    def give_reward(self,judge,case):
        #if at end give 0 reward
        # if not at end give -1 reward
        print("jjj",self.judges_specialities[judge])
        if self.judges_specialities[judge][case]==1:
            return 0
        else:
            return -1
    #Cases
    def new_case(self):
        case= np.random.choice(a=np.arange(self.num_of_case_classes), size=(1, 1), p=self.case_probability).item()
        hours=np.random.choice(a=np.arange(1,self.max_hours_for_case+1), size=(1, 1),p=self.hours_probability).item()
        return case,hours
    #Queues
    def add_in_queue(self,judge,case):
        self.queues[judge].put(case)

    # every day remove last case from queue
    def next_day(self):
        for i in range(self.num_of_judges):
            self.observation_space[i].get()

    def get_judge_schedule_length(self,judge):
        return self.observation_space[judge].qsize()
    #Judges
    def set_specialities_of_judges(self):
        while(1):
            total_sum=0
            spec=np.random.choice(a=[0, 1], size=(self.num_of_judges, self.num_of_case_classes),
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

class action_space(object):
    def __init__(self,num_of_judges):
        self.actions=[*range(num_of_judges)]
    def sample(self,available_judges):
        return np.random.choice(a=available_judges, size=(1, 1)).item()
    def __str__(self):
        return str(self.actions)