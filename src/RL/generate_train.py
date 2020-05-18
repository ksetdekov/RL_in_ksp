import pandas as pd
import gym.spaces
import os
from src.utils_common import check_folder
import rocket_lander_gym # нужен для работы среды gym RocketLander-v0

from src.utils_common import OBSERVATIONS_COL_NAMES


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
            # print("Info          ",info,end='/n/n')

        if done:
            print("Simulation done.")
            break

    init_df = add_episode_res(init_df, observations, rewards)
    env.close()

save_folder = 'src/RL/outputs/'
print(os.path.abspath(save_folder))
check_folder(save_folder)

print(os.path.exists(save_folder))
save_path = os.path.join(save_folder, 'train_data.csv')
init_df.to_csv(save_path, index=False)