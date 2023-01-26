from environment import judgesSchedule
import os
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common import results_plotter


def main():

    #initialize the environment
    num_of_judges = 3
    days_to_schedule = 3 # Schedule to for which availability is created
    num_of_trial_classes = 6 #d ifferent types of trials
    max_hours_for_case = 4 # Generate max workload


    env = judgesSchedule(num_of_judges,days_to_schedule, num_of_trial_classes,max_hours_for_case)

    episodes=50
    for episode in range(episodes+1):
        obs=env.reset()
        print(obs)
        done=False
        score=0

        while not done:
            env.render()
            action=env.action_space.sample()
            obs,reward,done,info=env.step(action)
            score+=reward
        print("Episode:{},Score:{}".format(episode,score))


    log_path=os.path.join('Training','Logs')
    model = DQN("MultiInputPolicy", env, verbose=1,tensorboard_log=log_path)
    model.learn(total_timesteps=10000, log_interval=4)




        
if __name__ == '__main__':
   main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
