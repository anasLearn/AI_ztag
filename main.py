# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:17:32 2017

@author: aanas / anasLearn / Anas Aamoum
"""

import playing_field as PF
import position as PST
import team as TM


timer_counter = 200
effect_time = 5

width = 29
height = 15

humans_1_starting_positions= [(1,1),
                              (1,2),
                              (1,3),
                              (1,4),
                              (1,10),
                              (1,11),
                              (1,12),
                              (1,13),
                              (1,14)]

humans_2_starting_positions= [(28,1),
                              (28,2),
                              (28,3),
                              (28,4),
                              (28,10),
                              (28,11),
                              (28,12),
                              (28,13),
                              (28,14)]

zombies_1_starting_positions= [(1,7)]
zombies_2_starting_positions= [(28,7)]

red_team = TM.team(name="Reds", num_zombies=1, num_humans=9, num_doctors=0)
blue_team = TM.team(name="Blues", num_zombies=1, num_humans=9, num_doctors=0)


def oneSimulation():
    """
    At the beginning of each step, a player defines its target, then moves towards it
    """
    test_field = PF.RectangularField(width, height)
    
    for pos in humans_1_starting_positions:
        test_field.players_team1.append(TM.Human(test_field, red_team, PST.Position(pos[0], pos[1]), 
                                                                                    speed = 0.5))
    for pos in zombies_1_starting_positions:
        test_field.players_team1.append(TM.Human(test_field, red_team, PST.Position(pos[0], pos[1]), 
                                                                                    speed = 0.5))
        
    for pos in humans_2_starting_positions:
        test_field.players_team1.append(TM.Human(test_field, blue_team, PST.Position(pos[0], pos[1]), 
                                                                                    speed = 0.5))
    for pos in zombies_2_starting_positions:
        test_field.players_team1.append(TM.Human(test_field, blue_team, PST.Position(pos[0], pos[1]), 
                                                                                    speed = 0.5))
        
        
    while test_field.getNumberOfHumans() > 0:
        test_field.manageInteracationsOfPlayers()
        test_field.movePlayers()
        test_field.updateStatesOfPlayers()
        
#        for player in test_field.players_team1:
#            print("team 1")
#            print(player, end = " ")
#        
#        for player in test_field.players_team2:
#            print("team 2")
#            print(player,  end = " ")
        



oneSimulation()


          
