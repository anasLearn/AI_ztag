# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:54:17 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import math
import random
import playing_field as PF
import position as PST


timer_counter = 200
effect_time = 5

class team(object):
    """
    
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
    def __init__(self, field, team, position, speed):
        """
        
        """
        assert type(field) == PF.RectangularField
        assert type(speed) == float or int
        assert speed >= 0, "speed must be a positive float"
    
        self.field = field
        self.position = position
        self.team = team
        self.speed = speed
        self.direction = random.randrange(360)
        self.target = None

    def getPlayerPosition(self):
        """
        Return the position of the robot.
        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getPlayerDirection(self):
        """
        Return the direction of the robot.
        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setPlayerPosition(self, position):
        """
        Set the position of the robot to POSITION.
        position: a Position object.
        """
        assert type(position) == PST.Position
        
        self.position.x = position.x
        self.position.y = position.y #Preferable to do affect it this way since position may change

    def setPlayerDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.
        direction: integer representing an angle in degrees
        """
        assert type(direction) == int and direction >= 0 and direction < 360

        self.direction = direction

    def updatePosition(self):
        """
        Simulate the raise passage of a single time-step.
        Move the player to a new position.
        """
        
        nextPosition = self.position.getNewPosition(self.target.position, self.direction, self.speed)
        if self.field.isPositionInField(nextPosition):
            self.position = nextPosition            
        else:
            self.setPlayerDirection(random.randrange(360))
            
    def calculateDistance(self, other):
        """
        
        """
        return math.sqrt((self.position.getX() - other.position.getX())**2 + (self.position.getY() - other.position.getY())**2)
            
    def selectTarget(self):
        """
        The player selects its target depending on its nature and its state
        """
        raise NotImplementedError # don't change this!


        
        
        
class Zombie(Player):
    """
    A zombie chases humans of the other team.
    """
    def __init__(self, field, team, position, speed):
        Player.__init__(self, field, team, position, speed)
        self.disable_timer = 0
        
    def selectTarget(self):
        """
        The zombie's target is the nearest human from the other team
        """
        self.target = None
        target_distance = (100, self)
        for player in self.field.players_team1 + self.field.players_team2:
            if player.team != self.team and type(player) == Human:
                distance = self.caculateDistance(self, player)
                if distance < target_distance[0]:
                    target_distance = (distance, player)
        self.target = target_distance[1]

        def __str__(self):
            return "Zombie"
        
class Human(Player):
    """
    A human goes through the different checkpoints to become a doctor
    if infected a human looks for a doctor of either team
    """
    def __init__(self, field, team, position, speed):
        Player.__init__(self, field, team, position, speed)
        self.infected = False
        self.infection_counter = 0
        self.checkpoints_reached = []

    def selectTarget(self):
        """
        The human's target is:
            The nearest un-reached checkpoint if the human is not infected
            The nearest doctor if the human is infected
        """
        self.target = None
        target_distance = (100, self)
        if not self.infected:            
            for chck in self.field.checkpoints:
                distance = self.calculateDistance(chck)
                if distance < target_distance[0]:
                    target_distance = (distance, chck)
                    
        else:
            for player in self.field.players_team1 + self.field.players_team2:
                if type(player) == Doctor:
                    distance = self.caculateDistance(self, player)
                    if distance < target_distance[0]:
                        target_distance = (distance, player)    
        
        self.target = target_distance[1]
        
    def __str__(self):
        return "Human"
                

class Doctor(Player):
    """
    A doctor tries to heal infected humans from the same team
    if there are none, The doctor moves randomly in the field
    """
    def __init__(self, field, team, position, speed):
        Player.init(self, field, team, position, speed)
        self.disable_timer = 0
        
    def selectTarget(self):
        """
        The doctor's target is the nearest infected human from the same team
        """
        self.target = None
        target_distance = (100, self)
        for player in self.field.players_team1 + self.field.players_team2:
            if type(player) == Human and player.team == self.team and player.infected == True:
                distance = self.caculateDistance(self, player)
                if distance < target_distance[0]:
                    target_distance = (distance, player)     
        
        self.target = target_distance[1]

    def __str__(self):
        return "Doctor"
        
        
        