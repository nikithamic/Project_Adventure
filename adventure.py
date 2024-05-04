import json
import sys

def load_map(filename):
    """ Load the map from a given filename. """
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
    """ Check if the map is valid based on room definitions and exits. """
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

def find_room(game_map, room_name):
    """ Find a room by name from the map. """
    for room in game_map['rooms']:
        if room['name'] == room_name:
            return room
    return None

def display_room(room):
    """ Display the current room's details. """
    print(f"> {room['name']}\n")
    print(room['desc'] + "\n")
    if 'items' in room:
        print(f"Items: {', '.join(room['items'])}\n")
    print(f"Exits: {' '.join(room['exits'].keys())}\n")

def parse_input(command, current_room):
    """ Parse user input to handle commands, dealing with ambiguities and partial inputs. """
    words = command.split()
    if not words:
        return None, "You must enter a command."

    cmd = words[0]
    args = words[1:] if len(words) > 1 else []

    if cmd in ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']:
        cmd = 'go'
        args = [cmd]

    if cmd == 'go':
        if not args:
            return None, "Please specify a direction to go."
        direction = args[0]
        if direction not in current_room['exits']:
            possible_directions = [dir for dir in current_room['exits'] if dir.startswith(direction)]
            if len(possible_directions) == 1:
                return ('go', possible_directions[0]), None
            elif len(possible_directions) > 1:
                return None, f"Did you want to go {' or '.join(possible_directions)}?"
            else:
                return None, f"There's no way to go {direction}."
        return ('go', direction), None

    elif cmd == 'get':
        if not args:
            return None, "What do you want to get?"
        item = ' '.join(args)
        items_in_room = current_room.get('items', [])
        matching_items = [it for it in items_in_room if it.startswith(item)]
        if len(matching_items) == 1:
            return ('get', matching_items[0]), None
        elif len(matching_items) > 1:
            return None, f"Did you mean {' or '.join(matching_items)}?"
        else:
            return None, f"There's no {item} here."

    return (cmd, args), None

def play_game(game_map):
    """ Main game loop: display rooms, handle commands, and manage game state. """
    current_room = find_room(game_map, game_map['start'])
    inventory = []

    while True:
        display_room(current_room)
        command = input("What would you like to do? ").strip().lower()
        parsed_command, error = parse_input(command, current_room)
        if error:
            print(error)
            continue
        action, args = parsed_command

        if action == 'quit':
            print("Goodbye!")
            break
        elif action == 'look':
            continue
        elif action == 'go':
            current_room = find_room(game_map, current_room['exits'][args[0]])
            print(f"You go {args[0]}.\n")
        elif action == 'get':
            item = args[0]
            current_room['items'].remove(item)
            inventory.append(item)
            print(f"You pick up the {item}.")
        elif action == 'inventory':
            if inventory:
                print("Inventory:")
                for item in inventory:
                    print(f"  {item}")
            else:
                print("You're not carrying anything.")
        else:
            print(f"Sorry, I don't understand '{command}'.")

def main():
    """ Entry point of the script, handle command-line arguments. """
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)

    game_map = load_map(sys.argv[1])
    if not validate_map(game_map):
        print("Invalid map file.", file=sys.stderr)
        sys.exit(1)

    play_game(game_map)

if __name__ == "__main__":
    main()