import pandas as pd
import gym
import gym.spaces
import rocket_lander_gym
import matplotlib.pyplot as plt
import seaborn as sns
from engineering_approach.utils import get_engine_angle, get_engine_burn, get_rcs_action, draw_col_graphs

env = gym.make('RocketLander-v0')
env.reset()
episodes = 100
observations = []
rewards = []

PRINT_DEBUG_MSG = True
observation = [0]*10
angle_speed = 0

for i in range(1000):
    env.render()
    
    rcs_action = get_rcs_action(observation)
    engine_angle = get_engine_angle(observation)
    engine_burn = get_engine_burn(observation)
    action = [engine_angle, engine_burn, rcs_action]
    
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
    
    
env.close()

draw_col_graphs(observations)
