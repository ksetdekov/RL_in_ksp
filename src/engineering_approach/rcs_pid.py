import pandas as pd
import gym.spaces

setangle = 0
pid_params =[100,1,0]
error_last=0

# cumulative_error = error_last+error_last
def calc_cum_error(obs_history, setpoints):
    obs_history_df=pd.DataFrame(obs_history).copy()
    errorhist = obs_history_df[2]-setpoints
    return errorhist

def get_rcs_bypid(observation, pid_params, error_hist, setangle = 0):

    """
    Import observations, pid parameters, default set angle
    output action for rcs
    """
    angle = observation[2]
    angle_vel = observation[-1]
    error = setangle-angle

    cum_error = sum(error_hist)
    action = error*pid_params[0]-cum_error*pid_params[1]
    return action

env = gym.make('RocketLander-v0')
env.reset()

PRINT_DEBUG_MSG = True
observation = [0] * 10
angle_speed = 0
obs_history=[observation]

for i in range(1000):
    env.render()
    errorhist =calc_cum_error(obs_history, setangle)
    rcs_action = get_rcs_bypid(observation, pid_params, errorhist, setangle)
    action = [0, 5, rcs_action]

    observation, reward, done, info = env.step(action)
    obs_history.append(observation)
    print('!'*30)
    print(len(calc_cum_error(obs_history, setangle)))
    print('!' * 30)
    if PRINT_DEBUG_MSG:
        print("Action Taken  ", action)
        print("Observation   ", observation)
        print("Reward Gained ", reward)
        print("Info          ", info, end='\n\n')

    if done:
        print("Simulation done.")
        break
env.close()