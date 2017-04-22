# How to use the simulation
The user can set the pre-conditions of the simulation in the file `data.py`

In the file `main.py`, the user can run one simulation with the the function `runSimulation`.
The parameters `num_of_times` indicates how many times the simulation will be executed.

When `runSimulation` is executed, a the user is asked to indicate the number of zombies in each team.

The function `runAllSimulations` runs all possible combination of games with all possible numbers of zombies at the start of the game. The results are registered in a file that the user can choose.
