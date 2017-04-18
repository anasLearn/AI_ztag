# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:17:32 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import gc
import pylab

import playing_field as PF
import position as PST
import team as TM

#To be implemented later
#timer_counter = 200
#effect_time = 5

#metric size of basket-ball field
width = 29
height = 15

#starting positions of both teams in opposite ends of the field
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

#red_team = TM.Team(name="Reds", num_zombies=1, num_humans=9, num_doctors=0) #team 1
#blue_team = TM.Team(name="Blues", num_zombies=1, num_humans=9, num_doctors=0) # team 2




def runSimulation(num_of_times):
    """
    At the beginning of each step, a player defines its target, then moves towards it
    """
    
    test_field = PF.Field(width, height)

    

    
    
    team1_humans = []
    team1_zombies = []
    team1_doctors = []

    team2_humans = []
    team2_zombies = []
    team2_doctors = []

    
    def numberOfElements(team, kind):
        number = 0
        for player in team:
            if player.kind == kind:
                number += 1
        return number
    
    def oneSimulation():
        team1 = []
        team2 = []
        for pos in humans_1_starting_positions:
            team1.append(TM.Player(test_field, team1, PST.Position(pos[0], pos[1]), speed=0.5, kind="Human"))
        for pos in zombies_1_starting_positions:
            team1.append(TM.Player(test_field, team1, PST.Position(pos[0], pos[1]), speed=0.5, kind="Zombie"))
                
        for pos in humans_2_starting_positions:
            team2.append(TM.Player(test_field, team2, PST.Position(pos[0], pos[1]), speed=0.5, kind="Human"))
        for pos in zombies_2_starting_positions:
            team2.append(TM.Player(test_field, team2, PST.Position(pos[0], pos[1]), speed=0.5, kind="Zombie"))
        
        test_field.addPlayers(team1, team2)
        
        while test_field.getNumberOfHumans() > 0:
            test_field.updateStatusOfPlayers()
            test_field.movePlayers()
            test_field.playersInteractions()

        team1_humans.append(numberOfElements(team1, "Human"))
        team1_zombies.append(numberOfElements(team1, "Zombie"))
        team1_doctors.append(numberOfElements(team1, "Doctor"))
        
        team2_humans.append(numberOfElements(team2, "Human"))
        team2_zombies.append(numberOfElements(team2, "Zombie"))
        team2_doctors.append(numberOfElements(team2, "Doctor"))
        gc.collect()


    for _ in range(num_of_times):
        oneSimulation()
    


    pylab.plot(team1_humans)
    pylab.show()
    
    pylab.plot(team2_humans)
    pylab.show()
    
    pylab.plot(team1_zombies)
    pylab.show()
    
    pylab.plot(team2_zombies)
    pylab.show()
    
    pylab.plot(team1_doctors)
    pylab.show()
    
    pylab.plot(team2_doctors)
    pylab.show()


    
runSimulation(5)          
