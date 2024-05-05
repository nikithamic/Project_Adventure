import json
import sys

def load_map(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def validate_map(game_map):
    if 'start' not in game_map or 'rooms' not in game_map:
        return False
    room_names = set()
    for room in game_map['rooms']:
        if 'name' not in room or 'desc' not in room or 'exits' not in room:
            return False
        if room['name'] in room_names:
            return False
        room_names.add(room['name'])
        for exit_room in room['exits'].values():
            if exit_room not in room_names:
                return False
    return True

def initialize_game(filename):
    game_map = load_map(filename)
    if game_map is None or not validate_map(game_map):
        print("Error: Invalid map file.", file=sys.stderr)
        sys.exit(1)
    return game_map

def get_room(game_map, room_name):
    for room in game_map['rooms']:
        if room['name'] == room_name:
            return room
    return None

def display_room(room):
    print(f"> {room['name']}\n")
    print(room['desc'] + "\n")
    if 'items' in room:
        print(f"Items: {', '.join(room['items'])}\n")
    print(f"Exits: {' '.join(room['exits'].keys())}\n")

def move_player(game_map, current_room, direction):
    if direction in current_room['exits']:
        return get_room(game_map, current_room['exits'][direction])
    else:
        return None

def pick_up_item(current_room, item, inventory):
    if 'items' in current_room and item in current_room['items']:
        current_room['items'].remove(item)
        inventory.append(item)
        print(f"You pick up the {item}.")
    else:
        print(f"There's no {item} anywhere.")

def game_loop(game_map):
    current_room = get_room(game_map, game_map['start'])
    inventory = []
    display_room(current_room)
    while True:
        try:
            command = input("What would you like to do? ").strip().lower()
        except EOFError:
            print("Use 'quit' to exit.") 
            continue  
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if command == 'quit':
            print("Goodbye!")
            break
        elif command == 'look':
            display_room(current_room)
        elif command.startswith('go'):
            direction = command[2:].strip()
            if not direction:
                print("Sorry, you need to 'go' somewhere.")
            else:
                next_room = move_player(game_map, current_room, direction)
                if next_room:
                    current_room = next_room
                    print(f"You go {direction}.\n")
                    display_room(current_room)
                else:
                    print(f"There's no way to go {direction}.")
        elif command.startswith('get '):
            item = command[4:].strip()
            if item:
                pick_up_item(current_room, item, inventory)
            else:
                print("Sorry, you need to 'get' something.")
        elif command == 'inventory':
            if inventory:
                print("Inventory:")
                for item in inventory:
                    print(f"  {item}")
            else:
                print("You're not carrying anything.")
        else:
            print(f"Sorry, I don't understand '{command}'.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)

    game_map = initialize_game(sys.argv[1])
    game_loop(game_map)

if _name_ == '_main_':
    main()