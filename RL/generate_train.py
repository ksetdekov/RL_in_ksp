import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import pandas as pd
import gym
import gym.spaces
import rocket_lander_gym

from utils import OBSERVATIONS_COL_NAMES, check_folder

def add_episode_res(existing_df, observations, rewards, columns=OBSERVATIONS_COL_NAMES):
    new_obs_df = pd.DataFrame(observations, columns=columns)
    new_obs_df = pd.concat([new_obs_df, pd.Series(rewards)], axis=1).rename(columns={0:'rewards'})
    
    return pd.concat([existing_df, new_obs_df])

env = gym.make('RocketLander-v0')
env.reset()
episodes = range(100)
observations = []
rewards = []
init_df = pd.DataFrame(None)

PRINT_DEBUG_MSG = True
observation = [0]*10

for ep in episodes:
    for i in range(1000):
        action = env.action_space.sample()
        observation,reward,done,info =env.step(action)
        observations.append(observation)
        rewards.append(reward)
        
        if PRINT_DEBUG_MSG:
            print("Action Taken  ",action)
            print("Observation   ",observation)
            print("Reward Gained ",reward)
            print("Info          ",info,end='\n\n')

        if done:
            print("Simulation done.")
            break
        
    init_df = add_episode_res(init_df, observations, rewards)   
    env.close()

init_df.to_csv('train_data.csv', index=False)