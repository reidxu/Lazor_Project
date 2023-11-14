# Lazor Solver
Developers: JiWon Woo, Lauren Conway, Reid Xu

# Introduction 
The "Lazors" game is available for download on mobile. The main goal of the game is to place blocks to reflect lasers from starting points to goal points.
In addition to blocks that can be moved by the player, some levels contain blocks that can not be moved, serving as obstacles or tools depending on the level. 

# Block Types
As mentioned previously, there are three types of blocks: reflector, refractor, and opaque. The blocks affect lasers in the following manner:
Reflector: reflects a laser by 45 degrees
Refractor: A laser that makes contact with this block will pass straight through and a duplicate laser will be created as if the refractory block was a reflector
Opaque: any laser that makes contact with the opaque block is stopped and no reflection occurs. 

# Board Layout
Each level takes place on a board. Each board has laser starting points that will shoot lasers at predetermined angles and goal points where lasers must pass through to beat the level.
On the board, there are defined positions where blocks are eligible to be placed, and each level comes with different types and quantities of available blocks. 

# Solution Approach
To solve levels in this game, we developed this code that would calculate all possible board configurations for a specified level. The code will then calculate the path
that lasers will take for each board configuration. If all goal points are hit by lasers by a configuration, that configuration is flagged as the solution. 

# File Input
To use this solver, boards should be fed into the code as '.bff' files. The grids should be preceded by "GRID START" and end with "GRID STOP" at the top and bottom of the grids. 



The key to define spaces and blocks on the board is given here: 
x = no block allowed
o = blocks allowed
A = fixed reflect block
B = fixed opaque block
C = fixed refract block

The same key above is used to define available movable blocks in this format:
A 2
C 1
For example, these lines define 2 available reflect blocks and 1 available refract block to be placed.

Laser starting positions and directions should be defined as such: 
L x y vx vy
Where (x,y) are the coordinates on the board, and (vx,vy) are the x and y components of the laser direction vector respectively. 

Finally, goal points should be defined as such: 
P x y

# Using the Solver

Open the Final_Solution.py file. Initialize a Grid() object with an argument of the .bff file you would like to find the solution for. 
Call the Grid.output_solution() function, and if a solution is found, a success message will be output and 
a filename-solution.txt file will be saved. The txt file will show the solution grid using the same key
that was used to communicate the board in the .bff input file. If no solution is found, a failure message will be given. 
