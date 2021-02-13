# DebugIt_things
My set of codes written for the Debug It competition.

# What is it?
Tic Tac Toe is a solved game, meaning that its every game will end up in a draw if both sides play fairly.
A side wins only if the other side makes a mistake.
The objective is to create a solid 3, horizontally, vertically, or either of the diagonally.

# About this project
This version of Tic Tac Toe is implemented in Python, using PyGame as its display library. 

#### Features
```
Can play against CPU as well as in multiplayer mode against someone else.
Take screenshots (I've no idea why I implemented this)
Read about the game in about section.
Can quit the game (Pretty handy feature)
```

## Dependency
pygame module.
Can be installed by following command.
  
> pip install pygame
  
Make sure Calibri font is installed in your PC. It's default in Windows.
    
# How to
```
Just run the T3A.py file after installing pygame.
Click on the home page to proceed.
The options menu takes input by arrow keys.
Then play with mouse click.
```

# Some fun
There is an intentional bug in this piece of code, which lets you win against CPU if you go through that specific sequence. 
Try to find that sequence.
Other than that specific bug, you'll never win.
```
The bug is quite straightforward though. You can find it easily in the get_comp function in the Game class.
```

# Bored with this old, small, boring game?
```
There's Flappy Birds game in the folder with same name. 
Do check it out.
Its dependency is same as Tic Tac Toe's.
```
