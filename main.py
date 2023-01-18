import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt

from environment import environment
from agent import Agent


def main():

    #initialize the environment
    num_of_judges = 3
    days_to_schedule = 3 # Schedule to for which availability is created
    num_of_trial_classes = 6 #d ifferent types of trials
    max_hours_for_case = 4 # Generate max workload
    N = 5 # number of episodes
    max_arrivals = 1 # Max number of arrivals per episode
    
    #Generate environment and define necesarry functions
    env = environment(num_of_judges, days_to_schedule, num_of_trial_classes,max_hours_for_case) #initialize the environment
    env.print_env()
    print("all possible states",list(env.all_possibilities()))

    #Agent is assigned to making decisions for the plan
    scheduler = Agent(env)
    
    #Step 0 initalization of rewards and state
    scheduler.init_reward(env.all_possibilities())
    print("values of states", scheduler.Q)
    done=0
    step=0
    print("start of the loop")
    
    # Iterations or time
    while not done:
        print("Next step ==============================")
        
        #Step 1: sample a new arrival (can done before starting the iteration, but also inside the iteration)
        case,hours=env.new_case()
        old_state=env.observation_space.copy()
        
        #Step 2a/b: Determine best decision based on current state,arrival of the case and Q value
        action = scheduler.assign_case_to_judge(env,env.observation_space, case, env.construct_allowed_states(env.observation_space))

        #Step 2c: update state baed on action chosen by scheduler
        reward,done=env.step(action)
        print("Step: ",step,"New case: ",case, "Action: ",action,"Old State: ", old_state, "New State: ", env.observation_space)
        step+=1










if __name__ == '__main__':
   main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
