import pandas as pd
import numpy as np
import gym.spaces
import os
from src.utils_common import check_folder
import rocket_lander_gym # нужен для работы среды gym RocketLander-v0

from src.utils_common import OBSERVATIONS_COL_NAMES, ACTIONS_COL_NAMES, REWARDS_COL_NAME, DEFAULT_SAVE_FOLDER
from src.engineering_approach.utils import get_engine_angle, get_rcs_action

def add_episode_res(existing_df, observations, action, rewards, episode_num, columns=OBSERVATIONS_COL_NAMES):
    new_obs_df = pd.DataFrame(observations, columns=columns)
    actions_df = pd.DataFrame(action).rename(columns={
        0: ACTIONS_COL_NAMES[0],
        1: ACTIONS_COL_NAMES[1],
        2: ACTIONS_COL_NAMES[2]
    })
    new_obs_df = pd.concat([new_obs_df, pd.Series(rewards)], axis=1).rename(columns={0: REWARDS_COL_NAME})
    new_obs_df = pd.concat([new_obs_df, actions_df], axis=1)
    new_obs_df['episode_num'] = episode_num
    return pd.concat([existing_df, new_obs_df])

def predict_burn_action(observation, engine_angle, rcs_action, train_predict_cols):
    predict_cols = train_predict_cols['pred_cols']
    model = train_predict_cols['model']
    
    action = [engine_angle, 0, rcs_action]
    train_df_full = pd.DataFrame(list(observation)+action).T
    train_df_full.columns = OBSERVATIONS_COL_NAMES + ACTIONS_COL_NAMES
    burn_action = max([0, model.predict(train_df_full[predict_cols])[0]])
    return burn_action

def filter_sessions_by_rewards(train_df, reward_quantile, sessions_num_thresh=200):
    sum_rewards = train_df.groupby('episode_num')['rewards'].sum().sort_values(ascending=False)
    if sessions_num_thresh:
        sum_rewards = sum_rewards[:sessions_num_thresh]
    elite_episode_nums = sum_rewards.loc[sum_rewards>=sum_rewards.quantile(reward_quantile)].index.values
    return train_df.loc[train_df['episode_num'].isin(elite_episode_nums), :]

def generate_random_sessions(starting_episode_num, episodes_num, save_filename='train_data.csv'):
    env = gym.make('RocketLander-v0')
    episodes = range(starting_episode_num, starting_episode_num+episodes_num)

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
        save_folder = DEFAULT_SAVE_FOLDER
        print('Saving observations to', os.path.abspath(save_folder))
        check_folder(save_folder)
        save_path = os.path.join(save_folder, 'train_data.csv')
        init_df.to_csv(save_path, index=False)
    return init_df

def generate_sessions(starting_episode_num, episodes_num, save_filename='train_data.csv',
                      train_predict_cols={}):
    env = gym.make('RocketLander-v0')
    episodes = range(starting_episode_num, starting_episode_num+episodes_num)

    init_df = pd.DataFrame(None)

    PRINT_DEBUG_MSG = False
    observation = [0]*10

    for ep in episodes:
        env.reset()
        observations = []
        actions = []
        rewards = []
        for i in range(10000):
            if train_predict_cols:
                rcs_action = get_rcs_action(observation)
                engine_angle = get_engine_angle(observation)
                burn_action = predict_burn_action(observation, engine_angle, rcs_action, train_predict_cols)
                action = [engine_angle, burn_action, rcs_action]
            else:
                action = env.action_space.sample()
                action[1] = np.random.choice(np.arange(0, 5, 0.001))
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
                # print(f"Simulation {ep} of {episodes_num} done.")
                break

        init_df = add_episode_res(init_df, observations, actions, rewards, episode_num=ep)
        env.close()
        
    if save_filename:
        save_folder = 'src/RL/outputs/'
        print('Saving observations to', os.path.abspath(save_folder))
        check_folder(save_folder)
        save_path = os.path.join(save_folder, 'train_data.csv')
        init_df.reset_index(drop=True).to_csv(save_path, index=False)
    return init_df.reset_index(drop=True)