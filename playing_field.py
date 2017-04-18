# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:37:07 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import random
import position as PST
import team as TM

class Checkpoint(object):
    """
    """
    def __init__(self, number, position):
        self.number = number
        self.position = position
        
        
class RectangularField(object):
    """
    A Rectangularfield represents a rectangular region (width * height)
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
        
        #Instantiate players of teams
        self.players_team1 = []
        self.players_team2 = []
        self.players = []

        #Checkpoints
        self.checkpoints = []
        
        for i in [1, 2, 3, 4]:            
            self.checkpoints.append(Checkpoint(i, self.getRandomPosition()))
            
        
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
        for player in self.players_team1 + self.players_team2:
            if type(player) == TM.Human:
                number += 1
        return number
        
    def manageInteracationsOfPlayers(self):
        for player1 in self.players_team1 + self.players_team2:
            for player2 in self.players_team1 + self.players_team2:
                if type(player1) == TM.Doctor and player1.disable_timer == 0:
                    if type(player2) == TM.Human:
                        player2.infected = False
                    if type(player2) == TM.Zombie:
                        if random.random() < 0.5:
                            player1.disable_timer = 20 if player1.disable_timer == 0 else player1.disable_timer
                        else:
                            player2.disable_timer = 20 if player2.disable_timer == 0 else player2.disable_timer
                            
                if type(player1) == TM.Human:
                    if type(player2) == TM.Zombie:
                        player1.infected = True
                        player1.checkpoints = [] 
                        
    def updateStatesOfPlayers(self):
        for player in self.players_team1 + self.players_team2:
            if type(player) in [TM.Doctor, TM.Zombie]:
                player.disable_timer -= 1
            else:
                if player.infected:
                    player.infection_counter += 1
                    if player.infection_counter == 20:
                        new_player = TM.Zombie(player.field, player.team, player.position, player.speed)
                        if player in self.players_team1:
                            self.players_team1.append(new_player)
                            self.players_team1.remove(player)
                        else:
                            self.players_team1.append(new_player)
                            self.players_team1.remove(player)
                            
                else:
                    for chck in self.checkpoints:
                        if player.calculateDistance(chck) < 1 and chck not in player.checkpoints_reached:
                            player.checkpoints_reached.append(chck)
                            
    def movePlayers(self):
        for player in self.players_team1 + self.players_team2:
            player.selectTarget()
            if self.isPositionInField(player.position.getNewPosition(player.target.position, player.direction, player.speed)):
                player.updatePosition()
                
        
        