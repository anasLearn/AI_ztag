# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:54:17 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import math
import random
import numpy as np


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
        
        self.rotate = random.choice(["clockwise", "c_clockwise"])
        
        #Attributes for "Human"
        self.reached_checkpoints = []
        self.infected = False #Becomes True when a "Zombie" infects "Human"
        self.to_infected_counter = 0 #when  healthy "Human" is near a "Zombie" this counter starts incrementing
        self.mark_checkpoint_counter = 0 #When healthy "Human" is near a "checkpoint" this counter starts incrementing
        self.to_zombie_counter = 0 #When a "Human" is infected, this counter starts incrementing
        self.to_healed_counter = 0 #when a "Human" is infected, and is near a "Doctor" this counter increments
        self.chased = False # If a zombie from the other team is nearby, this becomes True
        
        
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
        If the nextPosition is outside the field, the player changes its direction and attempts to move
        """
        

        if self.kind == "Zombie":
            #if there is a checkpoint nearby, the zombie gets away from it
            if self.checkpointNearby((self.x, self.y)):
                nextPosition = FN.getNewPosition(self.x, self.y, None, self.direction, self.speed, self.chased)
                while(not self.field.isPositionInField(nextPosition)):
                    self.direction = random.randrange(360)
                    nextPosition = FN.getNewPosition(self.x, self.y, None, self.direction, self.speed, self.chased)
            
            #This part of the code is tricky, to be reviewed in case of problem
            else:
                nextPosition = FN.getNewPosition(self.x, self.y, self.target, self.direction, self.speed, self.chased)
                while(not self.field.isPositionInField(nextPosition)):
                   self.direction = random.randrange(360)
                   nextPosition = FN.getNewPosition(self.x, self.y, None, self.direction, self.speed, self.chased)
                
                #Changing the direction is to make sure that the zombie doesn't just keep returning to the checkpoint zone in the same way, but instead keeps circling around it 
                self.direction = (self.direction + 90) % 360
   
       #Human or Doctor
        else:
            nextPosition = FN.getNewPosition(self.x, self.y, self.target, self.direction, self.speed, self.chased, self.rotate)
            while(not self.field.isPositionInField(nextPosition)):
                #if following (or running away from) the target will lead to a non permitted position, remove the target
                nextPosition = FN.getNewPosition(self.x, self.y, None, self.direction, self.speed, self.chased, self.rotate)
                #if following the direction will lead to a position outside the filed, change the direction
                if (not self.field.isPositionInField(nextPosition)):
                    self.direction = random.randrange(360)

                    
        #the 0.5m  distance condition here
        #To be removed if it makes the simulation too slow
        for player in self.field.all_players:
            if player != self and player.calculateDistance(self, coord = (nextPosition[0], nextPosition[1])) < 0.5:
                nextPosition = ( (nextPosition[0] + self.x) / 2, (nextPosition[1] + self.y) / 2)
                break
        
        self.x = nextPosition[0]
        self.y = nextPosition[1]            
        
            
            
            
    def calculateDistance(self, other, coord = None):
        """
        Calculate the distance from the current player to another player or checkpoint
        """
        if coord is not None:
            return math.sqrt((self.x - coord[0])**2 + (self.y - coord[1])**2)
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
            The nearest un-reached checkpoint wether the human is infected or not
            If there is no checkpoint and the human is infected, the target is the nearest doctor
        The human runs from the zombie if the latter is nearby
        """
        def zombieInTheWay(checkpoint):
            """
            Determines if a zombie is standing between the player and a specific checkpoint
            """
            A = np.array([checkpoint.x, checkpoint.y])
            B = np.array([self.x, self.y])
            for zombie in chasing:
                if self.calculateDistance(checkpoint) > self.calculateDistance(zombie):
                    C = np.array([zombie.x, zombie.y])
                    BA = A - B
                    BC = C - B
                    
                    angle = math.pi / 2
                    cosinus = 0
                    try:
                        cosinus = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))

                    except:
                        print("0 division")
                    if -1 <= cosinus and cosinus <= 1:
                        angle = np.arccos(cosinus)
                    

                    if angle <= math.pi / 4:
                        return True
            return False
            
        self.target = None
        #If the human is not chased anymore, change the rotation, so that the next time, the human runs in the other direction
        to_rotate = self.chased
        self.chased = False
        min_distance_zombie = 0
        min_distance_doctor = 0
        min_distance_checkpoint = 0
        chasing = []
        
        
        for player in self.field.all_players:                
            if player.team != self.team and player.kind == "Zombie" and player.disabled == False:
                if self.calculateDistance(player) < 5:
                    chasing.append(player)
                
        for checkpoint in self.field.checkpoints:
            if checkpoint not in self.reached_checkpoints:        
                #if no zombie in the way, consider this checkpoint
                if not zombieInTheWay(checkpoint) or ((not self.infected) and self.calculateDistance(checkpoint) < self.speed):
                    min_distance_checkpoint = FN.setTarget(min_distance_checkpoint, self, checkpoint)
        
        if self.target == None:
            for zombie in chasing:
                min_distance_zombie = FN.setTarget(min_distance_zombie, self, zombie)
                self.chased = True
            
            if min_distance_zombie < 1.5:
                self.target = None
                self.chased = False
                
        if self.target == None and self.infected:
            for player in self.field.all_players:
                if player.kind == "Doctor" and not player.disabled:
                   min_distance_doctor = FN.setTarget(min_distance_doctor, self, player)
                
        if to_rotate == True and self.chased == False:
            self.changeRotation()
        
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
            if self.to_enabled_counter >= DT.resolution * DT.disability_period:
                self.disabled = False
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
            if self.to_zombie_counter >= DT.resolution * DT.safe_period and self.zombiesNearby():
                self.kind = "Zombie"
                return
            if self.to_zombie_counter >= DT.resolution * DT.infection_period:
                self.kind = "Zombie"
                return
            if self.to_healed_counter >= DT.resolution * DT.effect_time:
                self.infected = False
                self.to_infected_counter = 0
                self.to_zombie_counter = 0
                self.to_healed_counter = 0 
                
        #if a zombie has been nearby for the effect_time, the human becomes infected
        else:
            if self.to_infected_counter >= DT.resolution * DT.effect_time:
                self.infected = True
                self.to_infected_counter = 0
                self.mark_checkpoint_counter = 0
                self.to_zombie_counter = 0
                self.to_healed_counter = 0
            

        
        number_of_checkpoints_nearby = 0
        for checkpoint in self.field.checkpoints:
            if checkpoint not in self.reached_checkpoints and self.calculateDistance(checkpoint) < DT.effect_distance:
                number_of_checkpoints_nearby += 1 #The condition of the if is True => There is a checkpoint nearby
                self.mark_checkpoint_counter += 1
                if self.mark_checkpoint_counter >= DT.resolution * DT.effect_time:
                    self.reached_checkpoints.append(checkpoint)
                    self.field.activateCheckpoint(checkpoint)
                    self.mark_checkpoint_counter = 0
                    self.infected = False
                    self.to_infected_counter = 0
                    self.to_zombie_counter = 0
                    self.to_healed_counter = 0 
        if number_of_checkpoints_nearby == 0:
            self.mark_checkpoint_counter = 0
        if len(self.reached_checkpoints) == DT.num_of_checkpoints:
            self.kind = "Doctor"
        

                
                
    def interactions(self):
        """
        The player updates its status, depending on its kind and current status
        """
        if self.kind == "Human":
            return self.humanInteractions()
            
    def humanInteractions(self):
        """
        Healthy humans are affected by zombies
        Infected humans are affected by doctors
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
        
        
    def checkpointNearby(self, position):
        distances = []
        for checkpoint in self.field.checkpoints:
            distances.append(math.sqrt((position[0] - checkpoint.x)**2 + (position[1] - checkpoint.y)**2))
        if distances != [] and min(distances) < DT.safe_zone:
            return True
        return False
        
    def zombiesNearby(self):
        for player in self.field.all_players:
            if player.team != self.team and player.kind == "Zombie" and not player.disabled and self.calculateDistance(player) < DT.effect_distance:
                return True
                
    def changeRotation(self):
        if self.rotate == "clockwise":
            self.rotate = "c_clockwise"
        else:
            self.rotate = "clockwise"
        
        