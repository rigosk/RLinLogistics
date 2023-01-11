import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt

from environment import Env
from agent import Agent

def main():
    num_of_judges = 3
    size_of_queues = 3#[4,30] #4 cases per day, 30 days
    num_of_trial_classes = 6 #different types of trials
    N = 10 #

    plan = Env(num_of_judges, size_of_queues, num_of_trial_classes)
    print("all possible states",list(plan.all_possibilities()))

    scheduler=Agent(plan)

    scheduler.init_reward(plan.all_possibilities())
    print("values of states",scheduler.G)
    for i in range(3):
        case=plan.new_case()
        state=plan.state
        #print("===>",state,case)


        action=scheduler.assign_case_to_judge(state,case,plan.construct_allowed_states(state))
        #print("State", plan.state,"Action",action)
        plan.update_state(case,action)
        print("State2", plan.state)




    print('==',plan.construct_allowed_states(plan.state))
    scheduler.print_G()
    scheduler.assign_case_to_judge(plan.state,plan.new_case(),plan.construct_allowed_states(plan.state))
    plan.print_env()
    print(plan.new_case())

    print(plan.is_speciality_of_judge(0, 2))

    plan.set_specialities_of_judges()


if __name__ == '__main__':
   main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
