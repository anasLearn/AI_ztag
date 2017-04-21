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
            checkpoint.x = DT.width * random.random()
            checkpoint.y = DT.height * random.random()
            
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
            player.interactions()
        

                        

                            

                
        
        