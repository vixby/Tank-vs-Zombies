# Zombie Survivors

Game created for a project in Computer Graphics at Reykjavik University.

Description

This is a simple game written in Python, using the OpenGL and pygame libraries. In this game, you control a tank to fight against a swarm of zombies while collecting supplies.

# Prerequisites

To run this game, you'll need the following:

    Python 3.x
    PyOpenGL
    pygame

You can install the required Python packages using pip:
pip install PyOpenGL pygame

How to Play

    Arrow or ASDW Keys: Move the tank
    Space Bar or Mouseclick: Shoot
    Escape: Quit game

Main features are:

- Realistic tank movement
- Zombies follow and face the tank
- Collision detection of the tank (forward, back and rotating)
- Collision detection of projectiles hitting zombies or bouncing off the walls in a realistic and accurate manner
- Supply boxes with different attributes
  - Health box to heal
  - Ammo box to increase max ammunition the tank can hold
  - Bomb box to spread chaos accross the map
- Five levels with increasing difficulty
- Beginning and an end to the game (With restart as an option)

Known bugs

- Collision with wall corners
  - Discovered late in the project without enough time to implement a fix
  - Plan is to do a point intersection detection between the corners of the tank body
