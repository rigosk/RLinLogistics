import numpy as np
import numpy.random as rand
from gym.spaces import Box,Dict,Discrete
from gym import Env
import numpy as np
class judgesSchedule(Env):
    def __init__(self,num_of_judges,specialities,days_to_schedule,max_hours_for_case):
        self.num_of_judges=num_of_judges
        self.num_of_specialities=specialities
        self.days_to_schedule=days_to_schedule
        self.max_hours_for_case=max_hours_for_case
        # Calculate arrival probabilities and hours for each case class
        self.case_probability = self.init_case_classes_probability(
            self.num_of_specialities)  # probability that a new case is of that class
        self.hours_probability = self.init_case_hours_probability(
            self.max_hours_for_case)  # probability of hours needed for a new case

        self.action_space=Discrete(self.num_of_judges)


        self.observation_space=Dict({"dayToSchedule": Box(low=0, high=self.days_to_schedule, shape=(self.num_of_judges,), dtype=np.int_),
                                     "speciality":Box(low=0, high=1, shape=(self.num_of_judges,self.num_of_specialities), dtype=np.int_),
                                     "totalHours": Box(low=0, high=self.max_hours_for_case*self.days_to_schedule, shape=(self.num_of_judges,), dtype=np.int_), #4 hours max per day
                                    "availability":  Box(low=0, high=1, shape=(self.num_of_judges,self.days_to_schedule), dtype=np.int_),#1 is available, 2 is not
                                     "next_case":Discrete(self.num_of_specialities),
                                     "hours":Discrete(self.max_hours_for_case)})

        availability =[]
        for t in (np.random.choice(a=[0, 1], size=(self.num_of_judges, self.days_to_schedule), p=[0.3,0.7])) : # p is the distribution of unavailibilty, we can adjust accordingly
            availability.append(t.tolist())




        self.state={"dayToSchedule":list(np.zeros(self.num_of_judges, dtype=int)),# day to Schedule
                    "speciality":list(self.set_specialities_of_judges()), #specialities matrix for each judge
                    "totalHours":list(np.zeros(self.num_of_judges, dtype=int)), # total hours of judge
                    "availability":(availability),
                    "next_case":self.new_case()[0],
                    "hours":self.new_case()[1]} #availability


        self.standard_deviation=0

        self.length=0
    def step(self,action):




        previous_std=self.standard_deviation=0
        #update state
        if  self.state["dayToSchedule"][action]<self.days_to_schedule-1:
            self.state["dayToSchedule"][action] +=1
        self.standard_deviation = np.std(self.state["totalHours"])

        # Calculate reward for the action before we change state

        reward = self.calculate_reward(action,self.state["next_case"],previous_std)




        #terminate episode
        self.length += 1
        if self.length<=np.sum(self.state["availability"]): # if all availabilities are covered
            done=0
        else:
            done=1


        info={}
        return self.state,reward,done,info




    def render(self):
        pass
    def reset(self):
        availability = []
        for t in (np.random.choice(a=[0, 1], size=(self.num_of_judges, self.days_to_schedule),
                                   p=[0.3, 0.7])):  # p is the distribution of unavailibilty, we can adjust accordingly
            availability.append(t.tolist())

        self.state = {"dayToSchedule": list(np.zeros(self.num_of_judges, dtype=int)),  # day to Schedule
                      "speciality": list(self.set_specialities_of_judges()),  # specialities matrix for each judge
                      "totalHours": list(np.zeros(self.num_of_judges, dtype=int)),  # total hours of judge
                      "availability": (availability),
                      "next_case": self.new_case()[0],
                      "hours": self.new_case()[1]}  # availability
        self.length = 0

        return self.state

    def new_case(self):
        case = np.random.choice(a=np.arange(self.num_of_specialities), size=(1, 1), p=self.case_probability).item()
        hours = np.random.choice(a=np.arange(0, self.max_hours_for_case ), size=(1, 1),
                                 p=self.hours_probability).item()
        return case, hours
        # Calculate probability case specialty

    def init_case_classes_probability(self, num_of_case_classes):
        '''initialize for the given number of case classes the probability that the may show when simulating '''
        a = np.random.random(num_of_case_classes)  # initialize random numbers for each trial class
        a /= a.sum()  # normalize
        return a

        # Calculate probability case duration

    def init_case_hours_probability(self, max_hours_for_case):
        h = np.random.random(max_hours_for_case)  # initialize random numbers for each trial class
        h /= h.sum()  # normalize
        return h

    def calculate_reward(self,action,case,previous_std):
        if self.state["dayToSchedule"][action] > self.days_to_schedule:  # if we have covered all days for a judge
            reward = -100
        elif self.state["availability"][action][
            self.state["dayToSchedule"][action]] == 0:  # if judge not available the day hi is scheduled
            reward = -100
        elif case not in self.state["speciality"][action]:  # if case is not in judge's specialities
            reward = -50
        elif self.standard_deviation > previous_std:
            reward = -10
        else:
            reward = -1
        return reward
    def set_specialities_of_judges(self):
        while(1):
            total_sum=0
            #If judge j can handle case i then 1, otherwise 0
            spec=np.random.choice(a=[0, 1], size=(self.num_of_judges, self.num_of_specialities),p=[0.7, 0.3])  # Random choosing between 0 and 1 based on p (the distribution), we can adjust accordingly
            for i in range(len(spec[0,:])):
                if spec[:,i].sum()>0:
                    total_sum=total_sum+1
                if total_sum==self.num_of_specialities: #Each speciality is assigned to at least one.
                    return spec.tolist()