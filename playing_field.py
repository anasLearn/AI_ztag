# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:37:07 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import random

import data as DT


class Checkpoint(object):
    """
    
    """
    def __init__(self, number):
        self.number = number
        self.x = 0
        self.y = 0
        
        print("Checkpoint %d Created" % number)
        
        
class Field(object):
    """
    A Field represents a rectangular region (width * height)
    """
    def __init__(self):
        """
        
        """
        #Checkpoints
        self.checkpoints = []        
        for i in range(DT.num_of_checkpoints):            
            self.checkpoints.append(Checkpoint(i + 1))
            
        print("Field Created")
        
    def getNewCheckpoints(self):
        """
        Used to set new checkpoints at the beginning of each game
        """
        for checkpoint in self.checkpoints:
            checkpoint.x = self.width * random.random()
            checkpoint.y = self.height * random.random()
            
    def addPlayers(self, team1, team2):
        self.all_players = team1 + team2
    

    def isPositionInField(self, pos):
        """
        returns: True if pos is in the field, False otherwise.
        """        
        if pos[0] >= 0 and pos[0] < DT.width:
            if pos[1] >= 0 and pos[1] < DT.height:
                return True
        return False
        
    def getNumberOfHumans(self):
        """
        Number of humans in the field
        As long as this number is > 0, the game continues
        """
        number = 0
        for player in self.all_players:
            if player.kind == "Human":
                number += 1
        return number
        
    def updateStatusOfPlayers(self):
        for player in self.all_players:
            player.updateStatus()

                        
    def movePlayers(self):
        for player in self.all_players:
            player.selectTarget()
            player.updatePosition()
        
        
    def playersInteractions(self):
        for player in self.all_players:
            player.manageInteractions()
        
#            for player2 in self.all_players:
#                if player1.calculateDistance(player2) < 1:
#                    if player1.kind == "Doctor" and player1.sick == False:
#                        if player2.kind == "Human":
#                            player2.sick = False
#                            player2.timer = 0
#                        # Doctor meets a Zombie : One of them will become sick
#                        if player2.kind == "Zombie" and player2.sick == False:
#                            if random.random() < 0.5:
#                                player1.timer = 200
#                                player1.sick = True
#                            else:
#                                player2.timer = 200
#                                player2.sick = True
#                                
#                    if player1.kind == "Human" and player1.sick == False:
#                        if player2.kind == "Zombie" and player2.sick == False:
#                            player1.sick = True
#                            player1.checkpoints = []
#                            player1.timer = 200 
                        

                            

                
        
        