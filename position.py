# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:58:04 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import math
# === 
class Position(object):
    """
    A Position represents a location in a two-dimensional field.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, target_position, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.
        Does NOT test whether the returned position fits inside the field.
        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed
        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        if target_position is not None:
            delta_y = speed * (target_position.getY() - old_y)
            delta_x = speed * (target_position.getX() - old_x)
        else:
            angle = float(angle)
            # Compute the change in position
            delta_y = speed * math.cos(math.radians(angle))
            delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)