# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:17:32 2017

@author: aanas / anasLearn / Anas Aamoum
"""

import pylab

import playing_field as PF
import position as PST
import player as TM



#To be implemented later
#timer_counter = 200
#effect_time = 5

#metric size of basket-ball field
width = 29
height = 15

#starting positions of both teams in opposite ends of the field
humans_1_starting_positions= [PST.Position(1,1),
                              PST.Position(1,2),
                              #PST.Position(1,3),
                              #PST.Position(1,4),
                              #PST.Position(1,10),
                              #PST.Position(1,11),
                              PST.Position(1,12),
                              PST.Position(1,13),
                              PST.Position(1,14)]

humans_2_starting_positions= [PST.Position(28,1),
                              PST.Position(28,2),
                              PST.Position(28,3),
                              PST.Position(28,4),
                              PST.Position(28,10),
                              PST.Position(28,11),
                              PST.Position(28,12),
                              PST.Position(28,13),
                              PST.Position(28,14)]

zombies_1_starting_positions= [PST.Position(1,7),
                               PST.Position(1,8),
                               PST.Position(1,6),
                               PST.Position(1,9),
                               PST.Position(1,5)]

zombies_2_starting_positions= [PST.Position(28,7)]

#red_team = TM.Team(name="Reds", num_zombies=1, num_humans=9, num_doctors=0) #team 1
#blue_team = TM.Team(name="Blues", num_zombies=1, num_humans=9, num_doctors=0) # team 2




def runSimulation(num_of_times):
    """
    At the beginning of each step, a player defines its target, then moves towards it
    """
    
    test_field = PF.Field(width, height)
    team1 = []
    team2 = []

    
    for pos in humans_1_starting_positions:
        team1.append(TM.Player(test_field, team1, pos, speed=0.35, kind="Human"))
    for pos in zombies_1_starting_positions:
        team1.append(TM.Player(test_field, team1, pos, speed=0.35, kind="Zombie"))
            
    for pos in humans_2_starting_positions:
        team2.append(TM.Player(test_field, team2, pos, speed=0.35, kind="Human"))
    for pos in zombies_2_starting_positions:
        team2.append(TM.Player(test_field, team2, pos, speed=0.35, kind="Zombie"))
    

    
    
    
    team1_zombies = []
    team1_doctors = []

    
    team2_zombies = []
    team2_doctors = []

    number_of_steps = [] #How many steps each simulation takes

    
    def numberOfElements(team, kind):
        number = 0
        for player in team:
            if player.kind == kind:
                number += 1
        return number
    
    def oneSimulation():
        i = 0    
        for pos in humans_1_starting_positions:
            team1[i].reinitialize(pos, kind="Human")
            i += 1
        for pos in zombies_1_starting_positions:
            team1[i].reinitialize(pos, kind="Zombie")
            i += 1
        
        
        i = 0
        for pos in humans_2_starting_positions:
            team2[i].reinitialize(pos, kind="Human")
            i += 1
        for pos in zombies_2_starting_positions:
            team2[i].reinitialize(pos, kind="Zombie")
            i += 1
        





        test_field.addPlayers(team1, team2)
        test_field.getNewCheckpoints()

        
        i = 0
        while test_field.getNumberOfHumans() > 0:
            test_field.updateStatusOfPlayers()
            test_field.movePlayers()            
            test_field.playersInteractions()
            i += 1
            
        number_of_steps.append(i)
            

        
        team1_zombies.append(numberOfElements(team1, "Zombie"))
        team1_doctors.append(numberOfElements(team1, "Doctor"))
        
        
        team2_zombies.append(numberOfElements(team2, "Zombie"))
        team2_doctors.append(numberOfElements(team2, "Doctor"))



    for j in range(num_of_times):        
        print("simulation number", j + 1, "running...", end=" ")
        oneSimulation()
        print("done")
    


    
    
    pylab.plot(team1_zombies)
    pylab.plot(team1_doctors)
    pylab.title("Team1 Number of Docotrs and Zombies at the end of each game")
    pylab.ylim(0, 10)
    pylab.legend(("Z", "D"))
    pylab.show()
    
    
    
    pylab.plot(team2_zombies)
    pylab.plot(team2_doctors)
    pylab.title("Team2 Number of Docotrs and Zombies at the end of each game")
    pylab.ylim(0, 10)
    pylab.legend(("Z", "D"))
    pylab.show()

    pylab.plot(number_of_steps)
    pylab.title("Number of time steps of each game. 10 time steps = 1 seconds")
    pylab.show()

        
