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

def get_item_by_partial_name(items, partial_name):
    matches = [item for item in items if partial_name in item]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"Did you want to get the {', '.join(matches[:-1])} or the {matches[-1]}?")
    else:
        return None

def get_direction_by_abbreviation(exits, abbreviation):
    matches = [direction for direction in exits if direction.startswith(abbreviation)]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"Did you want to go {' or '.join(matches)}?")
    else:
        return None

def handle_help():
    print("You can run the following commands:")
    print("  go ...")
    print("  get ...")
    print("  look")
    print("  inventory")
    print("  quit")
    print("  help")

def handle_go(current_room, game_map, direction):
    direction = get_direction_by_abbreviation(current_room['exits'], direction)
    if direction:
        current_room = get_room(game_map, current_room['exits'][direction])
        print(f"You go {direction}.\n")
        display_room(current_room)
    else:
        print(f"There's no way to go {direction}.")
    return current_room

def handle_get(current_room, inventory, item_name):
    if not item_name:
        print("Sorry, you need to 'get' something.")
    else:
        item = get_item_by_partial_name(current_room.get('items', []), item_name)
        if item:
            current_room['items'].remove(item)
            inventory.append(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item_name} anywhere.")

def handle_drop(current_room, inventory, item_name):
    item = get_item_by_partial_name(inventory, item_name)
    if item:
        inventory.remove(item)
        current_room.setdefault('items', []).append(item)
        print(f"You drop the {item}.")
    else:
        print(f"You don't have a {item_name} to drop.")

def handle_inventory(inventory):
    if inventory:
        print("Inventory:")
        for item in inventory:
            print(f"  {item}")
    else:
        print("You're not carrying anything.")

def play_game(game_map):
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
        elif command == 'help':
            handle_help()
        elif command.startswith('go') or command in current_room['exits']:
            direction = command[2:].strip() if command.startswith('go') else command
            current_room = handle_go(current_room, game_map, direction)
        elif command.startswith('get'):
            item_name = command[3:].strip()
            handle_get(current_room, inventory, item_name)
        elif command.startswith('drop '):
            item_name = command[5:].strip()
            handle_drop(current_room, inventory, item_name)
        elif command == 'inventory':
            handle_inventory(inventory)
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

if _name_ == '_main_':
    main()