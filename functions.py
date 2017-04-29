# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:58:04 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import data as DT

import math
# === 

    
def getNewPosition(old_x, old_y, target, angle, speed, chased):
    """
    Computes and returns the new Position after a single clock-tick has
    passed, with this object as the current position, and with the
    specified target, angle and speed.
    Does NOT test whether the returned position fits inside the field.
    target: the point the player is trying to reach. it can be None
    angle: number representing angle in degrees, 0 <= angle < 360
    speed: positive float representing speed
    Returns: a Position object representing the new position.
    """
    if target is not None:
        distance = math.sqrt((target.y - old_y)**2 + (target.x - old_x)**2)
        if distance == 0:
            delta_y = 0
            delta_x = 0
        else:
            delta_y = speed * (target.y - old_y)/distance
            delta_x = speed * (target.x - old_x)/distance
        if chased:
            delta_x = - delta_x
            delta_y = - delta_y
    else:
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
    # Add that to the existing position
    new_x = old_x + delta_x
    new_y = old_y + delta_y
    return (new_x, new_y)


        
def setTarget(min_distance, chaser, target):    
    distance = chaser.calculateDistance(target)
    if chaser.target is None:  
        min_distance = distance
        chaser.target = target
    elif distance < min_distance:
        chaser.target = target
        min_distance = distance
    return min_distance
    
def setStartingPosition(positions, num_of_zombies, abscissa):
    dist = DT.height / (num_of_zombies + 1)
    for i in range(num_of_zombies):
        positions.append((abs(abscissa - 2), (i + 1) * dist))
    dist = DT.height / (DT.team_size - num_of_zombies + 1)
    for i in range(DT.team_size - num_of_zombies):
        positions.append((abs(abscissa - 0.1), (i + 1) * dist))
        