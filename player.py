# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:54:17 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import math
import random


import data as DT
import functions as FN
    
    
class Player(object):
    """
    A player has three possible kinds: "Zombie", a "Human" or a "Doctor"
    """
    def __init__(self, field, team, position, kind):
        """
        
        """
        #Attributes from the parameters
        self.field = field
        self.team = team
        self.initialize(position, kind)
        
        print("player created")
        
        
        
    def initialize(self, position, kind):
        """
        reinitialize the attributes without creating a new instance
        """
        #Attributes from the parameters
        self.x = position[0]
        self.y = position[1]
        self.kind = kind
        
        #Automatically set attributes
        self.speed = DT.speed_range[0] + random.random() * (DT.speed_range[1] - DT.speed_range[0])
        self.direction = random.randrange(360)
        self.target = None
        
        
        #Attributes for "Human"
        self.reached_checkpoints = []
        self.infected = False #Becomes True when a "Zombie" infects "Human"
        self.to_infected_counter = 0 #when  healthy "Human" is near a "Zombie" this counter starts incrementing
        self.mark_checkpoint_counter = 0 #When healthy "Human" is near a "checkpoint" this counter starts incrementing
        self.to_zombie_counter = 0 #When a "Human" is infected, this counter starts incrementing
        self.to_healed_counter = 0 #when a "Huam" is infected, and is near a "Doctor" this counter increments
        
        
        #Attributes for "Doctor" and "Zombie"
        self.disabled = False #If this is True, the "Zombie" can't infect, and the "Doctor" can't heal
        self.to_disabled_counter = 0 #When "Doctor" is near "Zombie", this counter increments
        self.to_enabled_counter = 0 #When "Doctor" / "Zombie" is disbled, this counter increments
                        

    


    def __str__(self):
        return str(self.team) + " " + str(self.kind) + " " + "(%0.2f, %0.2f)" % (self.x, self.y)


    def updatePosition(self):
        """
        Simulate the raise passage of a single time-step.
        Move the player to a new position.
        A Player attempts to reach its target, or moves randomly (Doctor)
        If the nextPosition is outside the field, the player doesn't move and changes its direction
        """        
        nextPosition = FN.getNewPosition(self.x, self.y, self.target, self.direction, self.speed)
        if self.field.isPositionInField(nextPosition):
            self.x = nextPosition[0]
            self.y = nextPosition[1]            
        else:
            self.direction = random.randrange(360)
            
    def calculateDistance(self, other):
        """
        Calculate the distance from the current player to another player or checkpoint
        """
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
            
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
        The zombie's target is the nearest non-infected Human from the other team
        """
        self.target = None
        min_distance = 0        
        for player in self.field.all_players:
            #Follow the nearest "Human" from the other team who is not infected
            if player.team != self.team and player.kind == "Human" and not player.infected:
                min_distance = FN.setTarget(min_distance, self, player)
#                distance = self.calculateDistance(player)
#                if self.target is None:  
#                    min_distance = distance
#                    self.target = player
#                elif distance < min_distance:
#                    self.target = player
#                    min_distance = distance


    def humanSelectTarget(self):
        """
        The human's target is:
            The nearest un-reached checkpoint if the human is not infected
            The nearest active Doctor from either team, if the human is infected
        """
        self.target = None
        min_distance = 0
        if not self.infected:            
            for checkpoint in self.field.checkpoints:
                if checkpoint not in self.reached_checkpoints:
                    min_distance = FN.setTarget(min_distance, self, checkpoint)
#                    distance = self.calculateDistance(checkpoint)
#                    if self.target is None:
#                        min_distance = distance
#                        self.target = checkpoint
#                    elif distance < min_distance:
#                        min_distance = distance
#                        self.target = checkpoint
                    
        else:
            for player in self.field.all_players:
                if player.kind == "Doctor" and not player.disabled:
                    min_distance = FN.setTarget(min_distance, self, player)
#                    distance = self.calculateDistance(player)
#                    if self.target is None:  
#                        min_distance = distance
#                        self.target = player
#                    elif distance < min_distance:
#                        self.target = player
#                        min_distance = distance
                
        
    def doctorSelectTarget(self):
        """
        The doctor's target is the nearest infected human from the same team
        if there are none, The doctor moves randomly in the field
        """
        self.target = None
        min_distance = 0
        for player in self.field.all_players:
            if player.kind == "Human" and player.team == self.team and player.infected == True:
                min_distance = FN.setTarget(min_distance, self, player)
#                distance = self.calculateDistance(player)
#                if self.target is None:  
#                    min_distance = distance
#                    self.target = player
#                elif distance < min_distance:
#                    self.target = player
#                    min_distance = distance   
        
    def updateStatus(self):
        """
        The player updates its status, depending on its kind and current status
        """
        if self.kind == "Zombie":
            return self.zombieUpdateStatus()
        elif self.kind == "Human":
            return self.humanUpdateStatus()
        elif self.kind == "Doctor":
            return self.doctorUpdateStatus()
            
            
    def zombieUpdateStatus(self):
        """
        If Zombie is unable to infect, the counter of its inability period keeps incrementing until it 
        completes the disability period
        """
        if self.disabled:
            self.to_enabled_counter += 1
            if self.to_enabled_counter == DT.resolution * DT.disability_period:
                self.disabled = False
                self.to_disabled_counter = 0
                self.to_enabled_counter = 0                
        else: 
            if self.to_disabled_counter == DT.resolution * DT.effect_time:
                self.disabled = True                
                self.to_disabled_counter = 0
                self.to_enabled_counter = 0

    def doctorUpdateStatus(self):
        """
        If Doctor is unable to heal, the counter of its inability period keeps incrementing until it 
        completes the disability period
        """
        self.zombieUpdateStatus() #Since both Zombie and Doctor have similar behavior in status updating
                
#            player.timer = max(player.timer - 1, 0)
#            if player.timer == 0 and player.sick == True:
#                if player.kind != "Human":
#                    player.sick = False
#                else: # player is Human, then player becomes a zombie
#                    player.kind = "Zombie"
#            
#            elif player.sick == False and player.kind == "Human":
#                for checkpoint in self.checkpoints:
#                    if checkpoint not in player.reached_checkpoints and player.calculateDistance(checkpoint) < 1:
#                        player.reached_checkpoints.append(checkpoint)
#                if len(player.reached_checkpoints) == 4:
#                    player.kind = "Doctor"

        
        
        