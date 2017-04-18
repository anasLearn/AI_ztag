# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:37:07 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import random
import position as PST

class Checkpoint(object):
    """
    
    """
    def __init__(self, number, position):
        self.number = number
        self.position = position
        
        
class Field(object):
    """
    A Field represents a rectangular region (width * height)
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular field with the specified width and height.
        width: an integer > 0
        height: an integer > 0
        """
        assert type(width) == int and type(height) == int, "width or height is not integer"
        assert width > 0 and height > 0, "width or height is not positive numbers"
        
        self.width = width
        self.height = height
        
        
        #Checkpoints
        self.checkpoints = []
        
        for i in range(1,5):            
            self.checkpoints.append(Checkpoint(i, self.getRandomPosition()))
            
    def addPlayers(self, team1, team2):
        self.all_players = team1 + team2

        
    def getRandomPosition(self):
        """
        Return a random position inside the room.
        returns: a Position object.
        """
        return PST.Position(self.width * random.random(), self.height * random.random())    
    

    def isPositionInField(self, pos):
        """
        Return True if pos is inside the field.
        pos: a Position object.
        returns: True if pos is in the field, False otherwise.
        """
        assert type(pos) == PST.Position
        if pos.x >= 0 and pos.x < self.width:
            if pos.y >= 0 and pos.y < self.height:
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
            player.timer = max(player.timer - 1, 0)
            if player.timer == 0 and player.sick == True:
                if player.kind != "Human":
                    player.sick = False
                else: # player is Human, then player becomes a zombie
                    player.kind = "Zombie"
            
            elif player.sick == False and player.kind == "Human":
                for checkpoint in self.checkpoints:
                    if checkpoint not in player.reached_checkpoints and player.calculateDistance(checkpoint) < 1:
                        player.reached_checkpoints.append(checkpoint)
                if len(player.reached_checkpoints) == 4:
                    player.kind = "Doctor"
                        
    def movePlayers(self):
        for player in self.all_players:
            player.selectTarget()
            player.updatePosition()
        
        
    def playersInteractions(self):
        for player1 in self.all_players:
            for player2 in self.all_players:
                if player1.calculateDistance(player2) < 1:
                    if player1.kind == "Doctor" and player1.sick == False:
                        if player2.kind == "Human":
                            player2.sick = False
                            player2.timer = 0
                        # Doctor meets a Zombie : One of them will become sick
                        if player2.kind == "Zombie" and player2.sick == False:
                            if random.random() < 0.5:
                                player1.timer = 200
                                player1.sick = True
                            else:
                                player2.timer = 200
                                player2.sick = True
                                
                    if player1.kind == "Human" and player1.sick == False:
                        if player2.kind == "Zombie" and player2.sick == False:
                            player1.sick = True
                            player1.checkpoints = []
                            player1.timer = 200 
                        

                            

                
        
        