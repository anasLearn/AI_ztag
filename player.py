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
        self.speed = (DT.speed_range[0] + random.random() * (DT.speed_range[1] - DT.speed_range[0])) / DT.resolution
        self.direction = random.randrange(360)
        self.target = None
        
        
        #Attributes for "Human"
        self.reached_checkpoints = []
        self.infected = False #Becomes True when a "Zombie" infects "Human"
        self.to_infected_counter = 0 #when  healthy "Human" is near a "Zombie" this counter starts incrementing
        self.mark_checkpoint_counter = 0 #When healthy "Human" is near a "checkpoint" this counter starts incrementing
        self.to_zombie_counter = 0 #When a "Human" is infected, this counter starts incrementing
        self.to_healed_counter = 0 #when a "Human" is infected, and is near a "Doctor" this counter increments
        
        
        #Attributes for "Doctor" and "Zombie"
        self.disabled = False #If this is True, the "Zombie" can't infect, and the "Doctor" can't heal
        self.to_disabled_counter = 0 #When "Doctor" is near "Zombie", this counter increments
        self.to_enabled_counter = 0 #When "Doctor" / "Zombie" is disbled, this counter increments
                        

    


    def __str__(self):
        return self.kind[0:3] + " (%0.2f, %0.2f) " % (self.x, self.y)


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
        #Follow the nearest "Human" from the other team who is not infected        
        for player in self.field.all_players:
            
            if player.team != self.team and player.kind == "Human" and not player.infected:
                min_distance = FN.setTarget(min_distance, self, player)
        
        if self.target == None: #If all the humans of the other team are infected, follow them !
            for player in self.field.all_players:
                if player.team != self.team and player.kind == "Human" and player.infected:
                    min_distance = FN.setTarget(min_distance, self, player)


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
                    
        else:
            for player in self.field.all_players:
                if player.kind == "Doctor" and not player.disabled:
                    min_distance = FN.setTarget(min_distance, self, player)
                
        
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
            if self.to_disabled_counter >= DT.resolution * DT.effect_time:
                if random.random() < 0.5: #A possibility of 50% to become disabled
                    self.disabled = True
                    ###
                    self.to_disabled_counter = 0
                    self.to_enabled_counter = 0

    def doctorUpdateStatus(self):
        """
        If Doctor is unable to heal, the counter of its inability period keeps incrementing until it 
        completes the disability period
        """
        self.zombieUpdateStatus() #Since both Zombie and Doctor have similar behavior in status updating
        
    def humanUpdateStatus(self):
        """
        If a human is infected:
            a counter is incrementing to determine when he/she will turn to zombie
            IF the healing counter reaches the effect_time, the human is not infected anymore
        If a human is not infected, he/she either:
            validates new checkpoints
            becomes infected
        """
        if self.infected:
            self.to_zombie_counter += 1
            if self.to_zombie_counter == DT.resolution * DT.infection_period:
                self.kind = "Zombie"
            if self.to_healed_counter >= DT.resolution * DT.effect_time:
                self.infected = False
                
        else:
            number_of_checkpoints_nearby = 0
            for checkpoint in self.field.checkpoints:
                if checkpoint not in self.reached_checkpoints and self.calculateDistance(checkpoint) < DT.effect_distance:
                    number_of_checkpoints_nearby += 1 #The condition of the if is True => There is a checkpoint nearby
                    self.mark_checkpoint_counter += 1
                    if self.mark_checkpoint_counter == DT.resolution * DT.effect_time:
                        self.reached_checkpoints.append(checkpoint)
                        self.mark_checkpoint_counter = 0
            if number_of_checkpoints_nearby == 0:
                self.mark_checkpoint_counter = 0
            if len(self.reached_checkpoints) == DT.num_of_checkpoints:
                self.kind = "Doctor"
            #if a zombie has been nearby for the effect_time, the human becomes infected
            elif self.to_infected_counter >= DT.resolution * DT.effect_time:
                self.infected = True
                self.reached_checkpoints = []
                self.to_infected_counter = 0
                self.mark_checkpoint_counter = 0
                self.to_zombie_counter = 0
                self.to_healed_counter = 0
                
                
    def interactions(self):
        """
        The player updates its status, depending on its kind and current status
        """
        if self.kind == "Zombie":
            return self.zombieInteractions()
        elif self.kind == "Human":
            return self.humanInteractions()
        elif self.kind == "Doctor":
            return self.doctorInteractions()
            
    def zombieInteractions(self):
        """
        Zombies are affected by Doctors
        """
        number_doctors_nearby = 0
        for player in self.field.all_players:
            if player.kind == "Doctor" and not player.disabled and self.calculateDistance(player) < DT.effect_distance:
                self.to_disabled_counter += 1
                number_doctors_nearby += 1
        if number_doctors_nearby == 0:
            self.to_disabled_counter = 0
        
    def doctorInteractions(self):
        """
        Doctors are affected by Zombies
        """
        number_zombies_nearby = 0
        for player in self.field.all_players:
            if player.kind == "Zombie" and not player.disabled and self.calculateDistance(player) < DT.effect_distance:
                self.to_disabled_counter += 1
                number_zombies_nearby += 1
        if number_zombies_nearby == 0:
            self.to_disabled_counter = 0
            
    def humanInteractions(self):
        """
        Healthy humans are affected by zombies
        Infected humans are affect by doctors
        """
        if self.infected:
            number_doctors_nearby = 0
            for player in self.field.all_players:
                if player.kind == "Doctor" and not player.disabled and self.calculateDistance(player) < DT.effect_distance:
                    self.to_healed_counter += 1
                    number_doctors_nearby += 1
            if number_doctors_nearby == 0:
                self.to_healed_counter = 0
            
        else:
            number_zombies_nearby = 0
            for player in self.field.all_players:
                if player.kind == "Zombie" and not player.disabled and self.calculateDistance(player) < DT.effect_distance:
                    self.to_infected_counter += 1
                    number_zombies_nearby += 1
            if number_zombies_nearby == 0:
                self.to_infected_counter = 0
        
        
        