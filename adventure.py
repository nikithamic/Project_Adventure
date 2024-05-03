import json
import sys


class TextAdventureGame:
    def __init__(self, map_filename):
        self.load_map(map_filename)
        self.current_room = None  # Initialize current room to None
        self.player_inventory = []
        self.awaiting_direction_decision = False
        self.valid_direction_choices = []
        self.ambiguous_direction_command = ""

    def load_map(self, map_filename):
        try:
            with open(map_filename, "r") as file:
                self.game_map = json.load(file)
        except FileNotFoundError:
            print(f"Error: Map file '{map_filename}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in map file '{map_filename}'.")
            sys.exit(1)

    def display_room(self):
        try:
            room = self.game_map[self.current_room]
            print(f"> {room['name']}\n\n{room['desc']}\n")
            self.display_items(room)
            self.display_exits(room)
        except KeyError:
            print(f"Error: Current room '{self.current_room}' not found in the map.")
            sys.exit(1)

    # Other methods remain unchanged...

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)
    
    map_filename = sys.argv[1]
    game = TextAdventureGame(map_filename)
    
    # Initialize current room after loading the map
    game.current_room = 0
    
    game.display_room()
    
    while True:
        try:
            command = input("What would you like to do? ").lower()
            if command == "quit":
                game.quit_game()
            else:
                game.process_input(command)
        except EOFError:
            print("\nUse 'quit' to exit.")  # Handle Ctrl-D without exiting
        except KeyboardInterrupt:
            print("\n...")
            print("KeyboardInterrupt")
            sys.exit(0)

if __name__ == "__main__":
    main()