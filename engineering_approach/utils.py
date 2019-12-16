import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def check_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
            
def get_rcs_action(observation):  # reaction_control_system
    """
    Функция возвращает действие для пшикалки,
    динамически подстраиваясь под угол и угловую скорость
    """
    angle = observation[2]
    angle_vel = observation[-1]

    angle_lim = abs(angle_vel) / 2

    if (angle < angle_lim) & (angle > 0):
        if angle_vel > 0:
            # слева от нуля, вращение влево | отр. пшикалка
            action = -angle * angle_vel * 10
        else:
            # слева от нуля, вращение вправо | пол. пшикалка
            action = -angle * angle_vel * 10
    elif (angle > -angle_lim) & (angle < 0):
        if angle_vel > 0:
            # справа от нуля, вращение влево | отр. пшикалка
            action = angle * angle_vel * 10
        else:
            # справа от нуля, вращение вправо | положительная пшикалка
            action = angle * angle_vel * 10
    else:
        action = -angle * 10

    return action

def get_engine_angle(observation):
    return observation[-1]*1.5

def get_engine_burn(observation):
    y = observation[1]
    return .6 if y>0 else 4

def draw_col_graphs(observations, 
                    plot_name = 'latest_plot.png'):
    col_names = [
    'x_position',
    'y_position',
    'angle',
    'first_leg_indicator',
    'second_leg_indicator',
    'throttle',
    'engine_gimbal',
    'x_velocity',
    'y_velocity',
    'angular_velocity'
]   
    not_draw_cols = ['first_leg_indicator', 'second_leg_indicator']
    draw_cols = [i for i in col_names if i not in not_draw_cols]
    draw_df = pd.DataFrame(observations, columns = col_names)[draw_cols]
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=[23,10])
    for i, column in enumerate(draw_cols):
        sns.lineplot(x = draw_df.index,
                    y = draw_df[column],
                    ax=axes[i//4,i%4])
    plt.tight_layout()
    check_folder('engineering_approach/plots/')
    plt.savefig(f'engineering_approach/plots/{plot_name}')
