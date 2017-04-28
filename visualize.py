# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:52:08 2017

@author: aanas / anasLearn / Anas Aamoum
"""
import data as DT

from tkinter import *
import time


class GameVisualization:
    def __init__(self, field, team1, team2, delay = DT.sim_speed / DT.resolution):
        "Initializes a visualization with the specified parameters."
        
        self.team1 = team1
        self.team2 = team2
        self.field = field
        
        # Number of seconds to pause after each frame
        self.delay = delay
        
        #How many pixels in one meter
        self.one_meter = DT.window_size

        #dimensions of the canvas
        w_dim = 25 + DT.width * self.one_meter + 25
        h_dim = 25 + DT.height * self.one_meter + 25


        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=w_dim, height=h_dim)
        self.w.pack()
        self.master.update()

        # Draw the field
        x1, y1 = 25, 25
        x2, y2 = w_dim - 25, h_dim - 25
        self.w.create_rectangle(x1, y1, x2, y2, fill = "grey")
        
        #Draw the checkpoints
        for checkpoint in field.checkpoints:
            x = 25 + checkpoint.x * self.one_meter
            y = 25 + checkpoint.y * self.one_meter            
            self.w.create_rectangle(x-3, y-3, x+3, y+3, fill="black")
            
        
        
        self.players = None
        self.text = self.w.create_text(25, 0, anchor=NW, text=self._status_string(0))
        self.time = 0
        self.master.update()

    def _status_string(self, time):
        "Returns an appropriate status string to print."
        return "Time: " + str(time//DT.resolution) + " sec"



    def update(self, players):
        "Redraws the visualization with the players."

        # Delete all existing players.
        if self.players:
            for player in self.players:
                self.w.delete(player)
                self.master.update_idletasks()
        # Draw new players
        self.players = []
        for player in players:
            x, y = 25 + self.one_meter * player.x, 25 + self.one_meter * player.y
            if player.kind == "Doctor":
                color = "blue"
                if player.disabled:
                    color = "yellow"
            elif player.kind == "Human":
                color = "green"
                if player.infected:
                    color = "light green"
            elif player.kind == "Zombie":
                color = "red"
                if player.disabled:
                    color = "pink"

            if player.team == self.team1:
                sign = "1"
            elif player.team == self.team2:
                sign = "2"
            
            self.players.append(self.w.create_rectangle(x-10, y-10, x+10, y+10,fill=color))
            self.players.append(self.w.create_text(x, y, text=sign, fill = "black"))
        # Update text
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(25, 0, anchor=NW, text=self._status_string(self.time))
        self.master.update()
        time.sleep(self.delay)

    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()
        
