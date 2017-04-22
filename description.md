# ZTAG Simulation

## Objective
Create a simulation of the ztag game.

## Programming language
Python 3

## Background
#### Rules:
The game has humans, zombies, and doctors.

Human objective is to avoid zombies and find 4 checkpoints to become doctor.

Zombies want to infect humans and turn them into zombies. At first infection, human can still find a checkpoint or doctor to heal to normal status. If he does not get healed within 20 seconds be becomes a zombie. Zombies will want to avoid doctors because there is a 50% chance that their infection ability may become disabled for 20 seconds. It's also important to know that the more zombies there are,  the better chance of infecting a human. 

Doctors can heal infected humans. They must still avoid zombies as their healing abilits may become disabled for 20 seconds if they encounter a zombie (50% chance).


#### Game objective:
2 teams, each with 9 humans and 1 zombie player to start. Objective is to infect all of the opposing team into zombies while having your own humans become doctors. At the end of the round, all players are either zombies or doctors. Points are calculated based on difference in number of doctors on each team.  Example team A has 4 doctors and 6 zombies while team B has 1 doctor and 9 zombie. Therefore team A scores 3 points (4 - 1). After 10 rounds we see which team has the higher score.

#### Playing field:
In a basketball court sized arena there are 4 checkpoints placed randomly.

The two teams start from opposite sides of the field.


## Solution
#### Strategy
Each zombie chases the nearest healthy human of the other team. If all the humans of the other team are infected, the zombies chase them to make sure they don't get healed by a doctor.
Each Human goes through the checkpoints. If the Human is infected, he/she goes to the nearest doctor.
Each Doctor goes to the nearest infected human from the same team. If all the humans from the same team are healthy, the doctor moves randomly in the field.

#### 1st milestone:
Implement a simulation of the game with each team starting with 10 players (9 Humans + 1 Zombie)
Plot the result of the end of the game.

#### 2nd milestone
Optimize the code
Make the simulation possible with a different number of starting players as zombies

#### 3rd milestone
Visualize the simulation







