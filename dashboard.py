# -*- coding: utf-8 -*-
"""
Created on Wed May 17 01:15:24 2017

@author: aanas / anasLearn / Anas Aamoum
"""

from tkinter import *
from tkinter import messagebox
import data as DT
from simulation import runSimulation, runAllSimulations, visualizeSimulation

class Interface(Frame):
    
    """
    Main window. All widgets are attributes of this class
    """
    
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()
        
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("ztag Simulation")
        self.master.iconbitmap('favicon.png')

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        
        
        #Field part
        text = Label(self, text="Field:", font=(None, 20, "bold"))
        text.place(x=0, y=0)
        text = Label(self, text="Height:\n(in meters)", font=(None, 10))
        text.place(x=0, y=50)
        text = Label(self, text="Width:\n(in meters)", font=(None, 10))
        text.place(x=0, y=100)
        text = Label(self, text="# Checkpoints:", font=(None, 10))
        text.place(x=0, y=150)
        
        self.height_field = StringVar(value='15')
        line_text = Entry(self, textvariable=self.height_field, width=5)
        line_text.place(x=150, y=50)
        self.width_field = StringVar(value='29')
        line_text = Entry(self, textvariable=self.width_field, width=5)
        line_text.place(x=150, y=100)
        self.num_checkpoints = StringVar(value='4')
        line_text = Entry(self, textvariable=self.num_checkpoints, width=5)
        line_text.place(x=150, y=150)
        
        
        
        
        #Teams part
        text = Label(self, text="Teams:", font=(None, 20, "bold"))
        text.place(x=0, y=200)
        text = Label(self, text="Team size:", font=(None, 10))
        text.place(x=0, y=250)
        text = Label(self, text="# Zombies team1", font=(None, 10))
        text.place(x=0, y=300)
        text = Label(self, text="# Zombies team2", font=(None, 10))
        text.place(x=0, y=350)
        
        self.team_size = StringVar(value='10')
        line_text = Entry(self, textvariable=self.team_size, width=5)
        line_text.place(x=150, y=250)
        self.z1 = StringVar(value='3')
        line_text = Entry(self, textvariable=self.z1, width=5)
        line_text.place(x=150, y=300)
        self.z2 = StringVar(value='3')
        line_text = Entry(self, textvariable=self.z2, width=5)
        line_text.place(x=150, y=350)
        
        
        # creating the buttons
        boutton = Button(self, text="Visualize simulation", command=self.visualize_button)
        # placing the button on my window
        boutton.place(x=250, y=50)
        
        text = Label(self, text="# times:", font=(None, 10))
        text.place(x=250, y=170)
        self.num_times = StringVar(value='100')
        line_text = Entry(self, textvariable=self.num_times, width=5)
        line_text.place(x=320, y=170)
        boutton = Button(self, text="Run simulation", command=self.run_sim)
        # placing the button on my window
        boutton.place(x=250, y=200)
        
        text = Label(self, text="# times:", font=(None, 10))
        text.place(x=250, y=270)
        self.num_times_all = StringVar(value='100')
        line_text = Entry(self, textvariable=self.num_times_all, width=5)
        line_text.place(x=320, y=270)
        
        text = Label(self, text="Output file:", font=(None, 10))
        text.place(x=250, y=300)
        self.output = StringVar(value='output_results')
        line_text = Entry(self, textvariable=self.output, width=20)
        line_text.place(x=335, y=300)
        text = Label(self, text="(.csv)", font=(None, 10))
        text.place(x=450, y=300)
        boutton = Button(self, text="Run all simulations", command=self.run_all_sim)
        # placing the button on my window
        boutton.place(x=250, y=330)
        
    def get_variables(self):
        DT.height = int(self.height_field.get())
        DT.width = int(self.width_field.get())
        DT.num_of_checkpoints = int(self.num_checkpoints.get())
        DT.team_size = int(self.team_size.get())
        DT.z1 = int(self.z1.get())
        DT.z2 = int(self.z2.get())
        
        #initiate other variable
        DT.window_size = 5 * 150 / DT.height

            
        
    def visualize_button(self):
        try:
            self.get_variables()
        except:
            messagebox.showerror(
                "Incorrect parameters",
                "Check the values you entered"
                )
            return
        visualizeSimulation()
        
    
    def run_sim(self):
        try:
            self.get_variables()
            num_times = int(self.num_times.get())
        except:
            messagebox.showerror(
                "Incorrect parameters",
                "Check the values you entered"
                )
            return
        runSimulation(num_of_times = num_times, num_zomb_team1 = DT.z1, num_zomb_team2 = DT.z2)
    
    def run_all_sim(self):
        try:
            self.get_variables()
            num_times = int(self.num_times_all.get())
            filename = self.output.get() + ".csv"
        except:
            messagebox.showerror(
                "Incorrect parameters",
                "Check the values you entered"
                )
            return
        runAllSimulations(num_of_times = num_times, file_name=filename)
        

        
        
fenetre = Tk()

#size of the window
fenetre.geometry("500x400")


