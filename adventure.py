import json
import sys

class TextAdventure:
    def __init__(self, map_filename):
        self.load_map(map_filename)
        self.current_room = self.start_room
        self.inventory = []

    def load_map(self, map_filename):
        with open(map_filename, 'r') as file:
            data = json.load(file)
            self.start_room = data['start']
            self.rooms = {room['name']: room for room in data['rooms']}

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def print_room_description(self, room_id):
        room = self.get_room(room_id)
        if room:
            print(f"> {room['name']}\n{room['desc']}")
            if 'items' in room:
                print("Items:", ', '.join(room['items']))
            print("Exits:", ', '.join(room['exits'].keys()))
        else:
            print("Room not found.")

    def go(self, direction):
        room = self.get_room(self.current_room)
        if room and direction in room['exits']:
            self.current_room = room['exits'][direction]
            self.print_room_description(self.current_room)
        else:
            print("There's no way to go", direction + ".")

    def look(self):
        self.print_room_description(self.current_room)

    def get(self, item_name):
     room = self.get_room(self.current_room)
     if room and 'items' in room and item_name in room['items']:
        self.inventory.append(item_name)
        room['items'].remove(item_name)
        print(f"You pick up the {item_name}.")
        self.inventory()  # Call inventory method to print inventory after picking up
     else:
        print(f"There's no {item_name} anywhere.")

    def inventory(self):
        if self.inventory:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")
        else:
            print("You're not carrying anything.")

    def help(self):
        print("You can run the following commands:")
        print("  go ...")
        print("  get ...")
        print("  look")
        print("  inventory")
        print("  quit")
        print("  help")

    def play(self):
     self.print_room_description(self.current_room)
     while True:
        command = input("What would you like to do? ").strip().lower().split()
        if not command:
            continue
        verb = command[0]
        target = ' '.join(command[1:])
        if hasattr(self, verb):
            getattr(self, verb)(target)
        else:
            print("Sorry, I don't understand that command.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)
    
    map_filename = sys.argv[1]
    game = TextAdventure(map_filename)
    game.play()