# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:25:17 2017

@author: aanas / anasLearn / Anas Aamoum
"""

#The initial condition of the simulation. Can be modified at will

resolution = 10 # how many steps of simulation in one real second
effect_distance = 1 # The distance under which the interactions between players happen in meters
effect_time = 1 # how much time the players has to be next to each other to produce an effect in seconds
disability_period = 20 #The period the Doctor and Zombie are disabled after they meet (in seconds)
infection_period = 20 #The period a Human stays infected before he/she turns to a Zombie if not healed (in seconds)
speed_range = (2, 7) # Possible range of speed of players in m/s, the speed of each player is picked up randomly from this range
              
#size of the field
height = 15
width = 29
num_of_checkpoints = 4
window_size = 40 # change this if the visualization window is too big or too small


#Teams' size
team_size = 10


#simulation speed: the bigger the number the slower the simulation. 1 => real time
sim_speed = 1
