import json
import sys

class Room:
    def __init__(self, id, name, desc, exits, items=None, locked=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.exits = exits
        self.items = items if items else []
        self.locked = locked

class Command:
    def __init__(self, name, description, action):
        self.name = name
        self.description = description
        self.action = action

class GameEngine:
    def __init__(self, map_file):
        self.rooms, self.locked_doors = self.load_map(map_file)
        self.current_room = self.rooms[0]
        self.inventory = []
        self.commands = self.initialize_commands()

    def initialize_commands(self):
        return {
            "go": Command("go", "Move in a direction (e.g., 'go east')", self.go),
            "look": Command("look", "Look around the room", lambda: self.describe_room(self.current_room)),
            "get": Command("get", "Pick up an item (e.g., 'get key')", self.get_item),
            "inventory": Command("inventory", "Check your inventory", self.show_inventory),
            "quit": Command("quit", "Quit the game", lambda: self.quit_game()),
            "help": Command("help", "Show available commands", self.show_help)
        }

    def load_map(self, map_file):
        try:
            with open(map_file, 'r') as file:
                map_data = json.load(file)
                rooms = []
                locked_doors = {}
                for i, room in enumerate(map_data):
                    rooms.append(Room(i, room["name"], room["desc"], room["exits"], room.get("items"), room.get("locked")))
                    if room.get("locked"):
                        locked_doors[i] = room["locked"]
                return rooms, locked_doors
        except FileNotFoundError:
            print(f"Error: The file '{map_file}' was not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: The map file is not in valid JSON format.")
            sys.exit(1)

    def start_game(self):
        print("Welcome to the Mystical Castle Adventure!")
        while True:
            self.describe_room(self.current_room)
            command_input = input("What would you like to do? ").strip().lower()
            self.process_command(command_input)

    def describe_room(self, room):
        print(f"\n> {room.name}\n\n{room.desc}\n")
        print("Items:", ", ".join(room.items) if room.items else "No items")
        print("Exits:", " ".join(room.exits.keys()))

    def process_command(self, command_input):
        command_parts = command_input.split()
        command_name = command_parts[0]
        command_args = command_parts[1:]

        command = self.commands.get(command_name)
        if command:
            command.action(*command_args)
        else:
            print("Unknown command.")

    def go(self, direction):
        if direction in self.current_room.exits:
            next_room_id = self.current_room.exits[direction]
            if next_room_id in self.locked_doors and self.locked_doors[next_room_id] not in self.inventory:
                print(f"The door is locked. You need {self.locked_doors[next_room_id]} to open it.")
            else:
                self.current_room = self.rooms[next_room_id]
        else:
            print("You can't go that way.")

    def get_item(self, item):
        if item in self.current_room.items:
            self.current_room.items.remove(item)
            self.inventory.append(item)
            print(f"You picked up the {item}.")
        else:
            print("That item is not here.")

    def show_inventory(self):
        print("Inventory:", ", ".join(self.inventory) if self.inventory else "You're not carrying anything.")

    def show_help(self):
        print("Available commands:")
        for command in self.commands.values():
            print(f"  {command.name}: {command.description}")

    def quit_game(self):
        print("Goodbye!")
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)

    map_file = sys.argv[1]
    game = GameEngine(map_file)
    game.start_game()
