import json
import sys


def load_map(filename):
    try:
        with open(filename, 'r') as file:
            game_map = json.load(file)
            if 'start' not in game_map or 'rooms' not in game_map:
                raise ValueError("Map file is missing 'start' or 'rooms' key.")
            return game_map
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading map file: {str(e)}", file=sys.stderr)
        sys.exit(1)

def validate_map(game_map):
    room_names = set()
    for room in game_map['rooms']:
        if 'name' not in room or 'desc' not in room or 'exits' not in room:
            return False
        if room['name'] in room_names:
            return False
        room_names.add(room['name'])
    for room in game_map['rooms']:
        for exit_room in room['exits'].values():
            if exit_room not in room_names:
                return False
    return True

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


def handle_help(verbs):
    print("You can run the following commands:")
    for verb in verbs:
        print(f"  {verb}")

def handle_drop(current_room, inventory, item):
    if item in inventory:
        inventory.remove(item)
        current_room.setdefault('items', []).append(item)
        print(f"You drop the {item}.")
    else:
        print(f"You don't have '{item}' in your inventory.")

def get_exit_abbreviations(exits):
    abbreviations = {
        "n": "north",
        "s": "south",
        "e": "east",
        "w": "west",
        "nw": "northwest",
        "ne": "northeast",
        "sw": "southwest",
        "se": "southeast"
    }
    return {abbr: direction for abbr, direction in abbreviations.items() if direction in exits}

def get_matching_directions(exits, abbreviation):
    return [direction for direction in exits if direction.startswith(abbreviation)]

def play_game(game_map):
    current_room = get_room(game_map, game_map['start'])
    inventory = []
    verbs = ['go ...', 'get ...', 'drop ...', 'look', 'inventory', 'quit', 'help']

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
        elif command in current_room['exits']:
            current_room = get_room(game_map, current_room['exits'][command])
            print(f"You go {command}.\n")
            display_room(current_room)
        elif command in get_exit_abbreviations(current_room['exits']):
            direction = get_exit_abbreviations(current_room['exits'])[command]
            current_room = get_room(game_map, current_room['exits'][direction])
            print(f"You go {direction}.\n")
            display_room(current_room)
        elif command.startswith('go'):
            direction = command[3:].strip()
            if not direction:
                print("Sorry, you need to 'go' somewhere.")
            elif direction in current_room['exits']:
                current_room = get_room(game_map, current_room['exits'][direction])
                print(f"You go {direction}.\n")
                display_room(current_room)
            elif len(direction) == 1:
                matching_directions = get_matching_directions(current_room['exits'], direction)
                if len(matching_directions) == 1:
                    direction = matching_directions[0]
                    current_room = get_room(game_map, current_room['exits'][direction])
                    print(f"You go {direction}.\n")
                    display_room(current_room)
                elif len(matching_directions) > 1:
                    print(f"Did you want to go {' or '.join(matching_directions)}?")
                else:
                    print(f"There's no way to go {direction}.")
            else:
                print(f"There's no way to go {direction}.")
        elif command.startswith('get'):
            item = command[4:].strip()
            if not item:
                print("Sorry, you need to 'get' something.")
            elif 'items' in current_room and item in current_room['items']:
                current_room['items'].remove(item)
                inventory.append(item)
                print(f"You pick up the {item}.")
            else:
                print(f"There's no {item} anywhere.")
        elif command.startswith('drop'):
            item = command[5:].strip()
            if not item:
                print("Sorry, you need to 'drop' something.")
            else:
                handle_drop(current_room, inventory, item)
        elif command == 'inventory':
            if inventory:
                print("Inventory:")
                for item in inventory:
                    print(f"  {item}")
            else:
                print("You're not carrying anything.")
        elif command == 'help':
            handle_help(verbs)
        else:
            print(f"Sorry, I don't understand '{command}'.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)

    game_map = load_map(sys.argv[1])
    if not validate_map(game_map):
        print("Invalid map file.", file=sys.stderr)
        sys.exit(1)

    play_game(game_map)

if __name__ == '__main__':
    main()