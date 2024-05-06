# Adventure

## Nikitha Michael
## nmichael1@stevens.edu
## Stevens ID:20027667
## URL: https://github.com/nikithamic/Project_Adventure.git
## Course: CS 515-A
## Instructor: Michael Greenberg


## Time Spent 
An estimate of 49 hours each were spent on this project.

## Description

Welcome to our Text Adventure Game, a classic text-based exploration game. In this game, you navigate through various rooms, interact with objects, solve puzzles, and overcome challenges. The game is played entirely through text commands in a console or terminal.


## Installation

To play the Text Adventure Game, ensure that you have Python 3.8 or higher installed on your machine.

Clone the repository to your local machine:

```zsh
git https://github.com/nikithamic/Project_Adventure.git
```

## GamePlay Instructions

1. Starting the Game:
   * Run the game using python adventure.py [map filename].
    ```zsh
        python adventure.py loop.map
    ```
   * The game initializes in the starting room, as defined in the map file.
2. Navigating Rooms:
   * Use direction commands to move between rooms.
   * Example: north, n, east, e, etc.
3. Interacting with Items:
   * get-get [item] to pick up items.
   * drop-drop [item] to leave items in the current room.
   * Use partial names for items when unambiguous.
4. Managing Inventory:
   * Inventory-View current items using inventory .
5. General Commands:
   * Look- look to describe the current room again.
   * help-help for a list of commands.
   * quit-quit to exit the game.
   
## Map Configuration
The game's world is defined in a JSON file.
Each room in the file is a JSON object with attributes like name, desc, exits and items
Additional attributes locked, and winning_items are included to support the extentions implemented.

*Note: The Provided map in the repository covers all additional attributes and can be used to test our implemented extentions.*

## Extentions Implemented

### 1. Directions as Verbs

#### Usage
* Players can input directions as commands without the need for the go prefix.
* Example: Typing east or e is equivalent to go east.
* Benefit: Streamlines navigation, making movement commands more intuitive and direct.
  
#### Implementation
* Accepts direction names (north, east, etc.) or their abbreviations (n, e, etc.) as standalone commands equivalent to go [direction].
* 
#### Testing
* Directly input direction commands without the go prefix and check if the movement is correctly executed.

### 2. Drop

#### Usage
* Allows players to remove items from their inventory and leave them in the current room.
* Usage: drop [item name], e.g., drop key.
* Benefit: Enables strategic management of inventory and interaction with the game environment.

#### Implementation

* Adds functionality to remove items from the player's inventory and place them in the current room.

#### Testing

* Pick up an item using get, then use drop to remove it from inventory and ensure it is listed in the room's items.
  
### 3. Help 

#### Usage 
To access the help menu, simply enter help during gameplay.The help menu will then list all available commands.
Usage: help, e.g. You can run the following commands:
  go ...
  get ...
  drop ...
  look
  inventory
  quit
  help
Benefit: Quick reference to all available commands for easy understanding

#### Implementation

* Dynamically generates and displays the list of available commands, ensuring players have easy understanding.

#### Testing

* I gave the help command and got the expected commands

## Bugs 

Currently, there are no identified bugs or errors within the code; however, the code has not successfully passed the test cases provided on Gradescope. Further investigation and testing may be required to align with Gradescope's specific testing criteria. 

## How we tested the code

I thoroughly tested the functionality of my adventure game, ensuring its robustness and accuracy. My testing process involved creating various combinations of maps to validate the map loading and navigation functionalities. Additionally, I rigorously tested the game with all the provided verbs to ensure proper execution of actions such as moving between rooms (go), interacting with items (get), examining the surroundings (look), checking inventory (inventory), and exiting the game (quit).

Furthermore, I extensively tested the three extensions I implemented to enhance the game experience. This included testing the dynamic generation of help text to ensure that new commands are seamlessly integrated without necessitating manual updates to the help command. Through comprehensive testing, I verified the reliability and effectiveness of my adventure game, guaranteeing an engaging and immersive player experience.


## Issues Encountered

  * Encountered KeyError in display_room; resolved by adding error handling. 
  * Implemented resolution for ambiguous direction commands in go method by prompting user for clarification.
  * We also faced some difficulties implementing abbreviations for directions but we figured that out and resolved it
  * The output formatting took a lot of time too surprisingly, mainly trying to get the output of our game match the sample interaction provided to us in the project details. We had to pay a lot of attention to detail on capitalisation, white space, etc.
  * Inspite of all the outputs displaying correctly byte by byte, it still dosen't passes the test cases given on gradescope

## Sample Gameplay for extensions.

 python3 adventure.py loop.map
> A white room

You are in a simple room with white walls.

Exits: north northeast northwest east

What would you like to do? go n
Did you want to go north or northeast or northwest?
What would you like to do? north
You go north.

> A blue room

This room is simple, too, but with blue walls.

Items: key

Exits: east south

What would you like to do? get key
You pick up the key.
What would you like to do? inventory
Inventory:
key
What would you like to do? help
You can run the following commands:
go ..
get ...
drop ...
look
inventory
quit
help
What would you like to do? drop
Sorry, you need to 'drop' something.
What would you like to do? drop key
You drop the key.
