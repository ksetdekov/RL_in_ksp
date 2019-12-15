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