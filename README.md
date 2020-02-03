# MazeSolver
MazeSolver in python, generate a random maze and then solves it using the A* algorithm
the maze is generated with a **Recrusive Backtracker** alghorithm using depth-first search:  
https://en.wikipedia.org/wiki/Maze_generation_algorithm  
https://en.wikipedia.org/wiki/Depth-first_search  
https://github.com/ZaniLuca/MazeGenerator  

and then solved using the A* Start pathfinding alghorithm:  
https://www.geeksforgeeks.org/a-search-algorithm/  
https://github.com/ZaniLuca/A-Star
# How to install
Just run the Maze_Solver.py file, make sure to have pygame 1.9.6 installed, otherwise do:  
	```bash
	pip install -r requirements.txt
	```
or 	```bash
	pip3 install pygame
	```
to install the latest version of pygame
# Screenshots
![Solved](https://user-images.githubusercontent.com/59318963/73696304-54f03800-46dc-11ea-9771-17cf2b9d07ec.PNG)
![Generating](https://user-images.githubusercontent.com/59318963/73696305-54f03800-46dc-11ea-8e1f-14722947d327.PNG)
![Solving](https://user-images.githubusercontent.com/59318963/73696307-5588ce80-46dc-11ea-8edb-3af772670f37.PNG)

Special thanks to Daniel Shiffman from TheCodingTrain for the awesomes tutorials on **Recursive Backtraking** and **A Star Pathfinding**
https://www.youtube.com/user/shiffman