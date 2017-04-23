# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:17:32 2017

@author: aanas / anasLearn / Anas Aamoum
"""

import pylab
import statistics

import playing_field as PF
import player as PL
import functions as FN
import data as DT

#starting positions of both teams in opposite ends of the field
team1_starting_positions= []
team2_starting_positions= []

z1 = int(input("Enter number of zombies for Team 1: "))
z2 = int(input("Enter number of zombies for Team 2: "))

FN.setStartingPosition(team1_starting_positions, z1, 0)
FN.setStartingPosition(team2_starting_positions, z2, DT.width)
    

def runSimulation(num_of_times, num_zomb_team1 = z1, num_zomb_team2 = z2, plot=True, file=None):
    """
    Run the simulation for a number of times set with the parameter num_times
    Plot the results
    """

    
    test_field = PF.Field()
    team1 = []
    team2 = []

    #These variables count the number of victories of each team and the draws
    results = { "team1_victories" : 0, "team2_victories" : 0, "draws" : 0, "fail" : 0 }

    
    for _ in range(DT.team_size):
        team1.append(PL.Player(test_field, team1, (0, 0), kind="-"))
        team2.append(PL.Player(test_field, team2, (0, 0), kind="-"))

    #The following lists contain the number of doctors in each team at the end of each simulation (game)
    team1_doctors = []
    team2_doctors = []

    #The following lists contain the number of zombies in each team at the end of each simulation (game)
    team1_zombies = []
    team2_zombies = []
    
    #How many steps each simulation takes
    number_of_steps = [] 

    
    def numberOfElements(team, kind):
        number = 0
        for player in team:
            if player.kind == kind:
                number += 1
        return number
    
    def oneSimulation():
        i = 0    
        for pos in team1_starting_positions[0: num_zomb_team1]:
            team1[i].initialize(pos, kind="Zombie")
            i += 1
        for pos in team1_starting_positions[num_zomb_team1:]:
            team1[i].initialize(pos, kind="Human")
            i += 1       
        
        i = 0    
        for pos in team2_starting_positions[0: num_zomb_team2]:
            team2[i].initialize(pos, kind="Zombie")
            i += 1
        for pos in team2_starting_positions[num_zomb_team2:]:
            team2[i].initialize(pos, kind="Human")
            i += 1 
            
            
        test_field.addPlayers(team1, team2)
        test_field.getNewCheckpoints()

        
        failed = False
        while test_field.getNumberOfHumans() > 0:
            test_field.playersInteractions()
            test_field.movePlayers()
            test_field.updateStatusOfPlayers()
            i += 1

            if i > 1200 * DT.resolution:
                print("simulation taking too long")
                failed = True
                break

        number_of_steps.append(i)
            

        if not failed:
            team1_zombies.append(numberOfElements(team1, "Zombie"))
            team1_doctors.append(numberOfElements(team1, "Doctor"))        
            
            team2_zombies.append(numberOfElements(team2, "Zombie"))
            team2_doctors.append(numberOfElements(team2, "Doctor"))
    
            if team1_doctors[-1] > team2_doctors[-1]:
                results["team1_victories"] += 1
            elif team1_doctors[-1] < team2_doctors[-1]:
                results["team2_victories"] += 1
            else:
                results["draws"] += 1
        else:            
            results["fail"] += 1


    for j in range(num_of_times):        
        print("simulation number", j + 1, "running...", end=" ")
        oneSimulation()
        print("done, T1_Zom =", num_zomb_team1, "   T2_Zom =", num_zomb_team2)
    


    
    if plot:
        pylab.plot(team1_doctors, "ro")
        pylab.plot(team2_doctors, "y*")
        pylab.title("Number of doctors at the end of each game")
        pylab.ylim(-1, 11)
        pylab.legend(("T1", "T2"))
        pylab.show()      
        
    
        pylab.plot(number_of_steps)
        pylab.title("Number of time steps of each game. %d time steps = 1 seconds" % DT.resolution)
        pylab.show()

    print("Team 1: Number of zombies at the start: ", num_zomb_team1)
    print("Team 2: Number of zombies at the start: ", num_zomb_team2)
    print("Team 1 victories: ", results["team1_victories"])
    print("Team 2 victories: ", results["team2_victories"])
    print("Draws: ", results["draws"])
    print("Number of failed simulations: ", results["fail"])
    print("Team 1: Total number of Doctors:", sum(team1_doctors))
    print("Team 2: Total number of Doctors:", sum(team2_doctors))
    
    if file != None:
        file.write(str(DT.team_size) + ",")
        file.write(str(num_zomb_team1) + ",")
        file.write(str(num_zomb_team2) + ",")
        file.write(str(results["team1_victories"]) + ",")
        file.write(str(results["team2_victories"]) + ",")
        file.write(str(results["draws"]) + ",")     
        file.write(str(sum(team1_doctors)) + ",")
        file.write(str(sum(team2_doctors)) + ",")
        file.write(str(sum(team1_doctors) - sum(team2_doctors)) + "\n")
    
def runAllSimulations(num_of_times, file_name):
    results_file = open(file_name, 'w')
    results_file.write("Team_Size,T1_Zom,T2_Zom,T1_Victories,T2_Victories,Draws,T1_total_Doc,T2_total_Doc,Doctors_Difference\n")
    results_file.close()
    for i in range(1, DT.team_size):
        for j in range(i, DT.team_size):
            results_file = open(file_name, 'a')
            runSimulation(num_of_times, i, j, plot=False, file=results_file)
            results_file.close()
            
    print("All Simulations Ended\n")
    
    
        
        
        
        
        
        
        