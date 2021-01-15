import os

OBSERVATIONS_COL_NAMES = [
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

ACTIONS_COL_NAMES = [
    'engine_angle_action',
    'burn_action',
    'rcs_action'
]

REWARDS_COL_NAME = 'rewards'
DEFAULT_SAVE_FOLDER = 'src/RL/outputs/'

def check_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)