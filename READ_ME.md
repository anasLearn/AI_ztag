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

Infected human can also be healed if they check in an active checkpoint they haven't checked before.

When a human is infected, he/she has a safe period of 3 seconds. After that period, if he/she meets a zombie, he turn to a zombie immediately. Otherwise he/she will turn after 20 seconds, if not healed by a doctor or a checkpoint.

#### Checkpoints:
When a human checks a checkpoint, it remains active for 5 seconds, and then it deactivates for 10 seconds. When, a checkpoint is deactivated, humans can't check it.
When a checkpoint is active, zombies can't get near it.


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

Human also run away from zombies. If a zombie is standing between a human and the checkpoint he/she is trying to reach,  the human circles around the zombie, and then tries to run towards the checkpoint.
If the zombie is too close, the human runs away from it towards a checkpoint or in a randomly chosen direction.

![goes to checkpoint](https://raw.githubusercontent.com/anasLearn/ztag/master/images/1.JPG "goes to checkpoint")

![circles around](https://raw.githubusercontent.com/anasLearn/ztag/master/images/2.JPG "circles around")

#### 1st milestone:
Implement a simulation of the game with each team starting with 10 players (9 Humans + 1 Zombie)
Plot the result of the end of the game.

#### 2nd milestone
Optimize the code
Make the simulation possible with a different number of starting players as zombies

#### 3rd milestone
Visualize the simulation







