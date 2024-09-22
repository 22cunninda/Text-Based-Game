rooms = {
    'Great Hall': {'South': 'Bedroom', 'Items': ['key']},
    'Bedroom': {'North': 'Great Hall', 'East': 'Cellar', 'Items': ['Magic Potion']},
    'Cellar': {'West': 'Bedroom', 'North': 'Dining Room', 'Items': ['Chest', 'Sword']},
    'Dining Room': {'East': 'Bedroom', 'Enemy': {'Name': 'Undead Wizard', 'Health': 5}},
}

inventory = []  # Player's inventory
player_health = 10  # Player starts with 10 health
enemy_defeated = False  # Global variable to track if the enemy has been defeated

def display_room(room):
    """Display the current room and items."""
    print(f"You are in the {room}.")
    
    # Display items in the room
    if 'Items' in rooms.get(room, {}):
        items = rooms[room]['Items']
        if items:
            print(f"You see the following items: {', '.join(items)}")
    
    # Display any enemy in the room
    if 'Enemy' in rooms.get(room, {}) and not enemy_defeated:
        enemy = rooms[room]['Enemy']
        print(f"You encounter a {enemy['Name']}! Prepare for battle!")
    
    # Display available directions
    directions = [direction for direction in rooms[room] if direction not in ['Items', 'Enemy']]
    if directions:
        print(f"You can go in the following directions: {', '.join(directions)}")

def pick_up_item(room, item):
    """Pick up an item and add it to the inventory."""
    item = item.lower()  # Make item case-insensitive
    if 'Items' in rooms[room]:
        items = [i.lower() for i in rooms[room]['Items']]  # Convert items in the room to lowercase
        if item in items:
            inventory.append(item)
            rooms[room]['Items'] = [i for i in rooms[room]['Items'] if i.lower() != item]  # Remove the picked item
            print(f"You picked up the {item}.")
        else:
            print(f"There is no {item} here.")
    else:
        print("There are no items in this room.")

def battle(enemy):
    """Basic battle function."""
    global player_health
    global enemy_defeated
    
    print(f"Fighting {enemy['Name']}...")
    
    while enemy['Health'] > 0:
        action = input("Do you want to attack or flee? ").lower()
        
        if action == "attack":
            enemy['Health'] -= 1  # You deal 1 damage per attack
            print(f"You attack the {enemy['Name']}! Its health is now {enemy['Health']}.")
            
            if enemy['Health'] <= 0:
                print(f"You defeated the {enemy['Name']}!")
                enemy_defeated = True
                return True
        
        elif action == "flee":
            print("You fled the battle!")
            return False
        
        else:
            print("Invalid action. Try again.")
        
        # Enemy attacks back
        player_health -= 1
        print(f"The {enemy['Name']} attacks you! Your health is now {player_health}.")
        
        if player_health <= 0:
            print("You have been defeated! Game Over.")
            exit()

def navigate(rooms, current_room):
    """Allow the player to navigate between rooms and interact with items."""
    global enemy_defeated
    
    display_room(current_room)  # Display the initial room
    
    while current_room != "exit":
        try:
            # If there's an enemy and it hasn't been defeated, force battle
            if 'Enemy' in rooms[current_room] and not enemy_defeated:
                enemy = rooms[current_room]['Enemy']
                if not battle(enemy):
                    # If the player flees, send them back to the previous room
                    current_room = 'Bedroom'  # Adjust this as needed
                    display_room(current_room)
                    continue  # Skip the rest of the loop to avoid moving away before battle
            
            command = input("Enter a command (go [direction], pick up [item], or exit): ").lower()

            if command == "exit":
                current_room = "exit"
                print("Thanks for playing! Goodbye.")
            
            elif command.startswith("go "):
                direction = command.split(" ")[1]
                next_room = rooms.get(current_room, {}).get(direction.title())  # Capitalize direction
                
                if next_room:
                    current_room = next_room
                    display_room(current_room)
                    
                    # Check for an enemy encounter if you move into a new room
                    if 'Enemy' in rooms[current_room] and not enemy_defeated:
                        enemy = rooms[current_room]['Enemy']
                        if not battle(enemy):
                            current_room = direction.title()
                            display_room(current_room)
                
                else:
                    print("You can't go that way. Try another direction.")
            
            elif command.startswith("pick up "):
                # Handle multi-word item names
                item = command[len("pick up "):].strip()  # Get the item name after "pick up"
                pick_up_item(current_room, item)
            
            else:
                print("Invalid command. Try again.")
        
        except (IndexError, KeyError, EOFError):
            print("Error with the command. Please try again.")

def main(): 
# Set the initial room for the player to start in.
    current_room = 'Great Hall'
    navigate(rooms, current_room)

if __name__ == "__main__":
    main()
