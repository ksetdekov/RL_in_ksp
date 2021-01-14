import pandas as pd
import gym.spaces
import os
from src.utils_common import check_folder
import rocket_lander_gym # нужен для работы среды gym RocketLander-v0

from src.utils_common import OBSERVATIONS_COL_NAMES


def add_episode_res(existing_df, observations, action, rewards, episode_num, columns=OBSERVATIONS_COL_NAMES):
    new_obs_df = pd.DataFrame(observations, columns=columns)
    actions_df = pd.DataFrame(action).rename(columns={
        0: 'engine_angle_action',
        1: 'burn_action',
        2: 'rcs_action'
    })
    new_obs_df = pd.concat([new_obs_df, pd.Series(rewards)], axis=1).rename(columns={0:'rewards'})
    new_obs_df = pd.concat([new_obs_df, actions_df], axis=1)
    new_obs_df['episode_num'] = episode_num
    return pd.concat([existing_df, new_obs_df])

def generate_sessions(episodes_num, save_filename='train_data.csv'):
    env = gym.make('RocketLander-v0')
    episodes = range(episodes_num)

    init_df = pd.DataFrame(None)

    PRINT_DEBUG_MSG = False
    observation = [0]*10

    for ep in episodes:
        env.reset()
        observations = []
        actions = []
        rewards = []
        for i in range(10000):
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            observations.append(observation)
            actions.append(action)
            rewards.append(reward)

            if PRINT_DEBUG_MSG:
                print("Action Taken  ",action)
                print("Observation   ",observation)
                print("Reward Gained ",reward)
#                 print("Info          ",info,end='/n/n')

            if done:
                print(f"Simulation {ep} of {episodes_num} done.")
                break

        init_df = add_episode_res(init_df, observations, actions, rewards, episode_num=ep)
        env.close()
        
    if save_filename:
        save_folder = 'src/RL/outputs/'
        print('Saving observations to', os.path.abspath(save_folder))
        check_folder(save_folder)
        save_path = os.path.join(save_folder, 'train_data.csv')
        init_df.to_csv(save_path, index=False)
    return init_df