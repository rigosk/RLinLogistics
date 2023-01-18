import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt

from environment import Env
from agent import Agent

def main():
    #input values
    num_of_judges = 3
    size_of_queues = 3 #[4,30] #4 cases per day, 30 days, Workload must be calculated in hours, so convert to hours.
    num_of_trial_classes = 6 #different types/specialties of trials
    N = 10 # Number of iterations
    max_arrivals = 1
    
    #Generate environment and define necesarry functions
    plan = Env(num_of_judges, size_of_queues, num_of_trial_classes,max_arrivals)
    print("all possible states",list(plan.all_possibilities()))

    #Agent is assinged to making decisions for the plan
    scheduler=Agent(plan)
    
    # Step 0 initalization of rewards and state
    scheduler.init_reward(plan.all_possibilities(),plan.all_actions)
    print("values of states",scheduler.QTable)
    
    # Iterations or time(?)
    for i in range(3):
        #Step 1: sample a new arrival (can done before starting the iteration, but also inside the iteration)
        case=plan.new_case()
        print("New Case", case)
        state=plan.state
        
        #Step 2a/b: Determine best decision based on current state,arrival of the case and Q value
        action=scheduler.assign_case_to_judge(state,case,plan.construct_allowed_states(state))
        
        #Step 2c: update state baed on action chosen by scheduler
        plan.update_state(case,action)
        
        #Print information about state and allowed states 
        print("State", plan.state)
        print('==',plan.construct_allowed_states(plan.state))
        scheduler.print_QTable()
        plan.print_env()
        
        # Schedule assignes case to judge based on the state, new case and allowed states, all functions defined in the plan
        # scheduler.assign_case_to_judge(plan.state,plan.new_case(),plan.construct_allowed_states(plan.state))
        # plan.set_specialities_of_judges()


if __name__ == '__main__':
   main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
