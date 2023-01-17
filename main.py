import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt

from environment import environment
from agent import Agent


def main():

    #initialize the environment
    num_of_judges = 3
    days_to_schedule = 3
    num_of_trial_classes = 6 #different types of trials
    max_hours_for_case=4
    N = 5 # number of episodes

    env = environment(num_of_judges, days_to_schedule, num_of_trial_classes,max_hours_for_case) #initialize the environment

    env.print_env()
    print("all possible states",list(env.all_possibilities()))




    scheduler = Agent(env)

    scheduler.init_reward(env.all_possibilities())
    print("values of states", scheduler.Q)
    done=0
    step=0
    print("start of the loop")
    while not done:
        print("Next step ==============================")
        case,hours=env.new_case()
        old_state=env.observation_space.copy()
        action = scheduler.assign_case_to_judge(env,env.observation_space, case, env.construct_allowed_states(env.observation_space))

        reward,done=env.step(action)
        print("Step: ",step,"New case: ",case, "Action: ",action,"Old State: ", old_state, "New State: ", env.observation_space)
        step+=1










if __name__ == '__main__':
   main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
