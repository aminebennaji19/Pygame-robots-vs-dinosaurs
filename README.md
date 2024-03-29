# Robots_vs_Dinosaurs Game

## Project Description and Objectives

The goal of this project is to implement a simple game for robots vs dinosaurs.

* This game was implemented thanks to the reference mentioned below:
-  https://www.youtube.com/watch?v=o-6pADy5Mdg this tutorial is about using pygame to implement space invaders game.

## Main Deliverables

- A containerized solution using Docker.
- A REST API running the game (I used Flask).
- The Game simulation (I used pygame to implement the main scenarios and features).

## Environment

 - **docker** if you want to use docker container.
 - **Python 3.x**

## Game scenarios

- The robot can be controlled using the arrows of the keyboard.
- The implemented movements are move right, move left, move forward, move backward and also the diagonal possible combinations of these movements.
- A robot can attack dinosaurs and shoot laser with his main weapon using the space button of the keyboard.
- A robot can ignite dinosaurs by moving towards them (from the left, front, back and right).
- A robot can kill a dinosaur using 2 attacks, and once ignited by moving towards a dinosaur, it only needs 1 attack to kill it.
- A dinosaur can attack a robot by shooting laser towards it.
- There is a Monster dinosaur(with more health) that joins to our game from time to time.
- There are some obstacles that a robot can hide behind to take cover from dinosaur attacks.
- Each robot has 3 lives, once dead it can respawn with 50% of health before the game is over.
- For the scoring, attacking a red dinosaur will give you 100 points per hit, attacking a yellow dinosaur will give you 200 points and green dinosaurs will give you 300 point, whereas hitting the Monster dinosaur will give you 100 points per hit !
- Dinosaurs are fixed in the simulation space but you can make them moving to make the game harder by setting the **moving_dinosaurs** flag to **1** or **-1**.


## Running the Game on your local environment
- After cloning the repository, use this command to install the game requirements:

```
pip3 install -r requirements.txt
```

- Then, run the game using this command:

```
python3 run.py
```
- To have a different user experience, you can test the game with different settings by using these flags:

* **screen_width**: the width of the simulation space you want to create.(600 by default)
* **screen_height**: the height of the simulation space you want to create.(600 by default).
* **number_of_dinosaur_rows**: the number of dinosaurs per row.(3 by default)
* **number_of_dinosaur_cols**: the number of dinosaurs per column.(4 by default)
* **obstacle_amount**: the amount of obstacles to create for hiding.(4 by default)
**dinosaurs_shooting_timer**: the cooldown for dinosaurs weapon.(800 milliseconds by default)


* **dinosaurs_shooting_timer**: the cooldown for dinosaurs weapon.(800 milliseconds by default)
* **moving_dinosaurs**: an integer specifying whether dinosaurs are moving or not and the moving direction.(0 by default)

## Running the Game API on using Flask

- Use this command to run the game API using Flask:

```
python3 game_api.py
```
- A server running the game using Flask as a backend launches our game you can open the game and start playing by clicking the link that appears in the CLI. (mine is 192.168.1.8:3000)

## Running the Game on Docker

- First, you have to build the docker container using this command:

```
docker build -t game:latest -f core/docker/Dockerfile .
```
- After building the docker image, you have to grant the access to connect to the XServer for Linux by using this command:

```
xhost+
```
- Then to run the game main pipeline use this command:

```
docker run -it --rm  -p 3000 -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD:/robots_vs_dinosaurs/ -e DISPLAY=$DISPLAY  game:latest python3 /robots_vs_dinosaurs/run.py
```
- To run the game Flask API use this command:

```
docker run -it --rm  -p 3000 -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD:/robots_vs_dinosaurs/ -e DISPLAY=$DISPLAY  game:latest python3 /robots_vs_dinosaurs/game_api.py
```

- A server running the game using Flask insid as a backend launches our game inside the container, you can open the game and start playing by clicking the one of the links that appear in the CLI. (mine is 172.17.0.2:3000)

-Enjoy !
