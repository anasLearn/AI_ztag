# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:54:17 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import math
import random


class Team(object):
    """
    A team contains a number of players
    """
    def __init__(self, name, num_zombies, num_humans, num_doctors):
        """
        
        """
        self.name = name
        self.num_zombies = 1
        self.num_humans = 9
        self.num_doctors = 0
        self.players = []
    
    
class Player(object):
    """
    
    """
    def __init__(self, field, team, position, speed, kind):
        """
        
        """
        assert type(speed) == float or int
        assert speed >= 0, "speed must be a positive float"
    
        self.field = field
        self.team = team
        self.position = position
        self.speed = speed
        self.direction = random.randrange(360)
        self.target = None
        self.sick = False # Indicates Zombie unable to infect, or Doctor unable to heal or Human infected
        self.timer = 0 # When this timer reaches 0 and self.sick is True, the status of the player changes.
        self.kind = kind
        self.reached_checkpoints = []

    def __str__(self):
        return self.kind + self.position.__str__()


    def getPlayerPosition(self):
        """
        Return the position of the player.
        """
        return self.position
    
    def getPlayerDirection(self):
        """
        Return the direction of the player
        """
        return self.direction

    def setPlayerPosition(self, position):
        """
        Set the position of the player
        """
        
        self.position.x = position.x
        self.position.y = position.y #Preferable to do affect it this way since position may change

    def setPlayerDirection(self, direction):
        """
        Set the direction of the player to DIRECTION.
        direction: integer representing an angle in degrees
        """
        assert type(direction) == int and direction >= 0 and direction < 360

        self.direction = direction

    def updatePosition(self):
        """
        Simulate the raise passage of a single time-step.
        Move the player to a new position.
        """
        
        nextPosition = self.position.getNewPosition(self.target, self.direction, self.speed)
        if self.field.isPositionInField(nextPosition):
            self.position = nextPosition            
        else:
            self.setPlayerDirection(random.randrange(360))
            
    def calculateDistance(self, other):
        """
        Calculate the distance from the current player to another player or checkpoint
        """
        return math.sqrt((self.position.getX() - other.position.getX())**2 + (self.position.getY() - other.position.getY())**2)
            
    def selectTarget(self):
        """
        The player selects its target depending on its kind and its situtation (sick or not)
        """
        if self.kind == "Zombie":
            return self.zombieSelectTarget()
        elif self.kind == "Human":
            return self.humanSelectTarget()
        elif self.kind == "Doctor":
            return self.doctorSelectTarget()
       
        
    def zombieSelectTarget(self):
        """
        The zombie's target is the nearest human from the other team
        """
        self.target = None        
        for player in self.field.all_players:
            if player.team != self.team and player.kind == "Human":
                distance = self.calculateDistance(player)
                if self.target is None:  
                    min_distance = distance
                    self.target = player
                elif distance < min_distance:
                    self.target = player
                    min_distance = distance


    def humanSelectTarget(self):
        """
        The human's target is:
            The nearest un-reached checkpoint if the human is not infected
            The nearest doctor from either team, if the human is infected
        """
        self.target = None
        if not self.sick:            
            for checkpoint in self.field.checkpoints:
                if checkpoint not in self.reached_checkpoints:
                    distance = self.calculateDistance(checkpoint)
                    if self.target is None:
                        min_distance = distance
                        self.target = checkpoint
                    elif distance < min_distance:
                        min_distance = distance
                        self.target = checkpoint
                    
        else:
            for player in self.field.all_players:
                if player.kind == "Doctor":
                    distance = self.calculateDistance(player)
                    if self.target is None:  
                        min_distance = distance
                        self.target = player
                    elif distance < min_distance:
                        self.target = player
                        min_distance = distance
                
        
    def doctorSelectTarget(self):
        """
        The doctor's target is the nearest sick human from the same team
        if there are none, The doctor moves randomly in the field
        """
        self.target = None
        for player in self.field.all_players:
            if player.kind == "Human" and player.team == self.team and player.sick == True:
                distance = self.calculateDistance(player)
                if self.target is None:  
                    min_distance = distance
                    self.target = player
                elif distance < min_distance:
                    self.target = player
                    min_distance = distance   
        



        
        
        