from queue import Queue
import itertools
#import pandas as pd
import numpy as np
import numpy.random as rand

#np.roll(x2, 1, axis=0)


class environment(object):
    #initialization of the object Env.
    def __init__(self, num_of_judges, days_to_schedule, num_of_case_classes,max_hours_for_case, max_arrivals):
       
        #Input parameters
        self.num_of_judges = num_of_judges
        self.days_to_schedule = days_to_schedule
        self.num_of_case_classes = num_of_case_classes
        self.max_hours_for_case = max_hours_for_case
        self.max_arrivals = max_arrivals

        #Calculate arrival probabilities and hours for each case class
        self.case_probability = self.init_case_classes_probability(num_of_case_classes) #probability that a new case is of that class
        self.hours_probability = self.init_case_hours_probability(max_hours_for_case) #probability of hours needed for a new case

        #Generate resource environment, like specialties and availability
        self.available_judges=np.arange(num_of_judges) #if days of scheduled has exceeded for a judge then hebecomes not available anymore for scheduling
        self.judges_specialities=self.set_specialities_of_judges()
        self.judges_availability=self.init_judges_availability()
        
        #Generate all possible states
        self.all_states=self.all_possibilities()
        self.all_actions=self.gen_actions()
        
        #self.action_space=[*range(num_of_judges)] #judge where the case will be assigned to
        #self.action_space=action_space(num_of_judges)
        # Initialize observation state with all zero's, depends on the number of judges. Corresponds with current state.
        self.observation_state = list(np.zeros(num_of_judges, dtype=int))#,self.judges_availability[:,0],0]#hours per judge? + the case class
        self.case=self.new_case()

        #Initialize empty queues and schedule
        #Queue size equals maximal days to schedule, and determines state based on availability and assigned cases.
        #Unavailabilty of judge blocks a spot in the queue
        self.schedule=[]
        #self.queues=[]
        #for i in range(num_of_judges):
        #    self.queues.append(Queue(maxsize=days_to_schedule))
       
    #functions created in the environment
    
    #function is called from main after determining the action
    #action is in format of: 
    def step(self,action):
        done=0
        if action==None:
            done=1
        else:
            self.observation_state =self.new_state(action)
            '''
            if self.observation_state[action]==self.days_to_schedule:
                self.observation_state[action] = 999
            else:
                # Increment state with one for the judge to whom the case is assigned to 
                self.observation_state[action]+=1'''
        return   done
    
    def new_state(self,action):
        new_state=[]
        for j in range(len(action)):
            if action[j]==1 and self.observation_state[j]==self.days_to_schedule:
                new_state = 999
            else:
                # Increment state with one for the judge to whom the case is assigned to  
                new_state.append(self.observation_state[j]+action[j])
        return   new_state
    
    ''' Probably not used
    #Create state based on assigned cases and availability
    def available_state(self):
        returns the day that each judge is available after non-availability dates
        for judge in range(self.num_of_judges):
            if self.judges_availability[judge][self.observation_state[judge]]==0:
                self.observation_state[judge]=self.observation_state[judge]+1
    '''
    def reset(self):
        '''reset the environment'''
        self.__init__(self.num_of_judges, self.days_to_schedule, self.num_of_case_classes,self.max_hours_for_case, self.max_arrivals)

    #Calculate probability case specialty
    def init_case_classes_probability(self,num_of_case_classes):
        '''initialize for the given number of case classes the probability that the may show when simulating '''
        a = np.random.random(num_of_case_classes)  # initialize random numbers for each trial class
        a /= a.sum()  # normalize
        return a
    
    #Calculate probability case duration
    def init_case_hours_probability(self,max_hours_for_case):
        h = np.random.random(max_hours_for_case)  # initialize random numbers for each trial class
        h /= h.sum()  # normalize
        return h
    
    #Initialize availability
    def init_judges_availability(self):
        return np.random.choice(a=[0, 1], size=(self.num_of_judges, self.days_to_schedule),p=[0.3, 0.7])  # p is the distribution of unavailibilty, we can adjust accordingly
 
    #Print arrival probability of each class  
    def print_case_classes_probability(self):
        print('Probabilities for the arriving cases are: ')
        print('Class \t Probability')
        for i in range(len(self.case_probability)):
            print(i, "\t:", self.case_probability[i])
            
    #Print arrival probability of each class  
    def print_case_hours_probability(self):
        print('Probabilities for the hours per case: ')
        print('hours \t Probability')
        for i in range(len(self.hours_probability)):
            print(i+1, "\t:", self.hours_probability[i])
    
    #Print information about judges and current queue length when called and ethe specialties of the judges.
    def print_env(self):
        self.print_case_classes_probability()
        self.print_case_hours_probability()
        print("\n Observation_state:")
        print(self.observation_state, "\n")
        print("Judges Availability:")
        print(self.judges_availability, "\n")
        #print("Action Space:")
        #print(self.action_space)
        print("Judges specialities")
        print(self.judges_specialities, "\n")
        print("Possible Actions:")
        print(self.all_actions, "\n")
        print("All possible states: ")
        print(self.all_states)

    ''' Probably not used, state is updated in step function
    # state of the env object based on the case and the action (action is given by scheduler)
    def update_state(self,case,action):

        temp=[]
        self.queues[action].put(case)

        for i in range(len(self.queues)):
            print("lll", list(self.queues[i].queue))
            temp.append(self.queues[i].qsize())
            self.observation_space=temp
    '''     
    
    # Create possible next states and therefore actions.
    # To Do: Incorporate the specialty, is not done yet.     
    # To Do: Check if observation state is update correctly. It looks like it takes the initilized state of [0,0,0]
    def construct_allowed_states(self,state,all_actions):
        '''Creating the allowed states after the current state
        cand_states=[]
        allowed_states=[]
        allowed_moves={}

        #Loop over all judges
        for i in range(len(self.observation_state)):
            #If judge isn't fully booked up to end of schedule and judge is not available, state of judge +1
            while ((self.observation_state[i] < self.days_to_schedule )and (self.judges_availability[i][self.observation_state[i]] == 0)):
                self.observation_state[i] += 1

            if (self.observation_state[i]<self.days_to_schedule)and (self.judges_availability[i][self.observation_state[i]]>0): # if a judge has not reach the limit of the queue
                #print("lalala", self.judges_availability, i, state[i])
                cand_states.append(i)
                
        for st in cand_states:

            #allowed_states.append(state.copy())
            #allowed_states[-1][st]=allowed_states[-1][st]+1

            allowed_states=self.observation_state.copy()
            allowed_states[st] = allowed_states[st] + 1
            allowed_moves[st]=allowed_states
            #print("from",state,"to",allowed_moves[st])
            '''
            
        '''Creating the allowed actions after the current state'''
        cand_actions = all_actions
        allowed_actions = all_actions
        a=0  
        # #Loop over all candidate states    
        # for a in range(len(cand_actions)):
        #     for j in range(len(self.observation_state)):
        #     #Determine per cand state if is possible,allowed if judge is fully booked
        #         if not(cand_actions[a][j]+ self.observation_state[j] < self.days_to_schedule):
        #             del allowed_actions[a]        
        #     #Add specialty, if not a soft constraint
         
        #Loop over all candidate states    
        while a < len(cand_actions):
            for j in range(len(self.observation_state)):
            #Determine per cand state if is possible,allowed if judge is fully booked
                if not(cand_actions[a][j]+ self.observation_state[j] < self.days_to_schedule):
                    del allowed_actions[a] 
                    a-=1
                    break
            a+=1
            #Add specialty, if not a soft constraint   
        return allowed_actions
    
    
    #Generates all possible states, state is number of cases in queue for each judge
    #To do: Change state from queue to schedule with blocks, all possible states when making an assignment choice depends on the possible allocations and availability of the judges
    #To do: Look-up differenct with function below  
    def all_possibilities(self):
        '''creates all possible states'''
       
        #if you want list to return
        #return (list(tup) for tup in itertools.combinations(range(self.size_of_queues),self.num_of_judges))
    
        #if you want tuples
        #return itertools.combinations(range(self.size_of_queues),self.num_of_judges
        all_states = list(itertools.product(range(self.days_to_schedule), repeat=self.num_of_judges))
        return all_states
    
    
    '''
    #function is not called, so not used. But needs to be called istead of definition above. 
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
        '''   
          
    #Generate all possible actions. 
    #At each decision epoch the arrived cased must be assigned to a judge
    def gen_actions(self): 
        actions = []
        prod = itertools.product(range(self.max_arrivals+1),repeat = self.num_of_judges)
        actions = list(prod)
        #print("Generated Actions", actions)
        i=0    
        while i < len(actions):
            if not sum(actions[i])== self.max_arrivals:
                del actions[i]
                i-= 1
            i+=1
        print("Possible Actions", actions)
        return actions     
    

    #Calculate direct reward C(St,Xt)
    #To do: base reward on deviation from average workload over the judges and deviation from the average index level (indicator timeline).
    def give_reward(self,state, action, case):
        #if at end give 0 reward
        #if not at end give -1 reward
        #print("jjj",self.judges_specialities[judge])
        reward = 0
        for a in range(len(action)):
            if action[a]==1:
                if self.judges_specialities[action[a]][case]==0:  
                    reward = reward - 1
        return reward 
        
    #Step 1: Generate new case, determines transition to new state. Corresponds with sample path Wn
    def new_case(self):
        case= np.random.choice(a=np.arange(self.num_of_case_classes), size=(1, 1), p=self.case_probability).item()
        hours=np.random.choice(a=np.arange(1,self.max_hours_for_case+1), size=(1, 1),p=self.hours_probability).item()
        return case,hours
    
    #Step 2c: Add case to chose queue
    #To do: Change queue to a schedule with availability blocks 
    def add_in_queue(self,judge,case):
        self.queues[judge].put(case)
    
    #Every day remove last case from queue
    #To do: Delete when schedule with availability blocks is used in algorithm. Removing cases is not necessary, because time element is included.
    def next_day(self):
        for i in range(self.num_of_judges):
            self.observation_state[i].get()
    
    def get_judge_schedule_length(self,judge):
        return self.observation_state[judge].qsize()
    
    #Function returns a matrix with 1 and 0
    #To do: verify is changing the indices doesn't corrupt the program (e.g. assigning the cases to judges)
    '''
    def set_specialities_of_judges(self):
        while(1):
            total_sum=0
            #If judge j can handle case i than 1, otherwise 0
            spec=np.random.choice(a=[0, 1], size=(self.num_of_judges, self.num_of_case_classes),
                                  p=[0.7, 0.3])  # p is the distribution, we can adjust accordingly
            for i in range(len(spec[:,0])):
                if spec[i,:].sum()>0:
                    total_sum=total_sum+1
            if total_sum==self.num_of_judges:
                return spec
    '''     
    def set_specialities_of_judges(self):
        while(1):
            total_sum=0
            #If judge j can handle case i than 1, otherwise 0
            spec=np.random.choice(a=[0, 1], size=(self.num_of_judges, self.num_of_case_classes),p=[0.7, 0.3])  # Random choosing between 0 and 1 based on p (the distribution), we can adjust accordingly
            for i in range(len(spec[0,:])):
                if spec[:,i].sum()>0:
                    total_sum=total_sum+1
                if total_sum==self.num_of_case_classes: #Each speciality is assigned at least ones. 
                    return spec
     
    #Returns true if judge j has specialty i        
    def is_speciality_of_judge(self,judge,speciality):
        return self.judges_specialities[judge,speciality]
    
    #Returns array with all specialties of judge j
    def get_judge_specialities(self,judge):
        return self.judges_specialities[judge, :]
    
    def keywithminval(self,d):
        """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
        v = list(d.values())
        k = list(d.keys())
        return k[v.index(min(v))]
   
'''
# Object to define action space, depends on
class action_space(object):
    def __init__(self,num_of_judges):
        self.actions=[*range(num_of_judges)]
    def sample(self,available_judges):
        return np.random.choice(a=available_judges, size=(1, 1)).item()
    def __str__(self):
        return str(self.actions)
'''