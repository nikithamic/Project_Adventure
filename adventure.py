import json
import sys

def load_map(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        sys.stderr.write(f"Failed to load map: {e}")
        sys.exit(1)

def find_room_by_name(rooms, name):
    return next((room for room in rooms if room['name'] == name), None)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        return

    map_filename = sys.argv[1]
    game_map = load_map(map_filename)
    current_room = find_room_by_name(game_map['rooms'], game_map['start'])
    player_inventory = []

    while True:
        print(f"> {current_room['name']}\n")
        print(current_room['desc'])
        print("\nExits:", " ".join(current_room['exits'].keys()))
        if 'items' in current_room:
            print("Items in the room:", ", ".join(current_room['items']))
        print("\nWhat would you like to do?")
        
        command = input().strip().lower()
        words = command.split()

        if not words:
            continue

        if words[0] == 'quit':
            print("Goodbye!")
            break

        elif words[0] == 'look':
            continue

        elif words[0] == 'go':
            if len(words) < 2:
                print("Sorry, you need to 'go' somewhere.")
                continue
            direction = words[1]
            if direction in current_room['exits']:
                current_room = find_room_by_name(game_map['rooms'], current_room['exits'][direction])
            else:
                print("There's no way to go", direction)

        elif words[0] == 'get':
            if len(words) < 2:
                print("Sorry, you need to 'get' something.")
                continue
            item = words[1]
            if 'items' in current_room and item in current_room['items']:
                current_room['items'].remove(item)
                player_inventory.append(item)
                print("You pick up the", item)
            else:
                print("There's no", item, "anywhere.")

        elif words[0] == 'inventory':
            if player_inventory:
                print("Inventory:", ", ".join(player_inventory))
            else:
                print("You're not carrying anything.")

        else:
            print("I don't understand that command.")

if _name_ == "_main_":
    main()