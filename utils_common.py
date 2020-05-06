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

def check_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)