import sys
import colorama

up = colorama.Cursor.UP
back = colorama.Cursor.BACK

colorama.init()

name = str(input('Podaj literke: '))
print(back() + up() + "Welcome to a humble little screen control demo program")

#Clear the screen
#screen_code = "\033[2J";
#sys.stdout.write( screen_code )

# Go up to the previous line and then
# clear to the end of line
screen_code = "\033[1A\033[K"
sys.stdout.write(screen_code)
a = input("What a: ")
a = a.strip()
sys.stdout.write(screen_code)
b = input("What b: ")
b = b.strip()
sys.stdout.write(screen_code)
print(f"a = {a}")
print(f"b = {b}")

for line in sys.stdin:
    print(line)

class Character:
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        self.inventory = {
            "albums": [],
            "instruments": []
        }
        self.coordinates = {
            'n': 0,
            'e': 0,
            's': 0,
            'w': 0
        }

    def get_inventory(self):
        print(self.inventory)

    def get_coordinates(self):
        print(self.coordinates)

    def str_coordinates(self):
        to_string = [str(v) for k, v in self.coordinates.items()]

        return ' '.join(to_string)

    def __str__(self):
        return  self.name

class Map:
    def __init__(self, *args):
        self.rooms = [*args]

    def get_room(self, room_coordinates):
        current_room = ''

        for room in self.rooms:
            if room.coordinates == room_coordinates:
                current_room = room

        return current_room

    def get_rooms(self):
        rooms_str = ''
        for room in self.rooms:
            rooms_str += room.coordinates + "\n"

        return rooms_str

class Room:
    def __init__(self, coordinates, name, actions, items, next_rooms):
        self.coordinates = coordinates
        self.name = name
        self.actions = actions
        self.items = items
        self.next_rooms = next_rooms

    def str_actions(self):
        return ', '.join(self.actions)

    def get_items_types(self):
        items_types = [item.item_type for item in self.items]
        return items_types

    def get_items_names(self):
        items_names = [item.name for item in self.items]
        return items_names

    def __str__(self):
        return self.name

class Item:
    def __init__(self, item_type, name):
        self.item_type = item_type
        self.name = name

class Album(Item):
    def __init__(self, item_type, name, lyrics):
        super().__init__(item_type, name)
        self.lyrics = lyrics

    def __str__(self):
        return self.item_type

ttng_animals = Album("Album", "Animals",
                     "Let's talk about facts, the very best moment we have")

math_rock_3 = Album("Album", "Math rock 3",
                    "Doesn't__init__ know the lyrics, play awesome guitar solo with tapping")

sort_of = Album("Album", "A test",
                    "Doesn't__init__ know the lyrics, play awesome guitar solo with tapping")

standard_actions = ["look", "move", "coordinates", "inventory", "take"]

player = Character("Mabuelalelelejando", "male")

start = Room("0 0 0 0", "Start", standard_actions, [math_rock_3, ttng_animals, sort_of], ['n'])
room_2 = Room("1 0 0 0", "Room 2", standard_actions, [("instrument", "nya")] , ['s'])

game_map = Map(start, room_2)

def update_north():
    if player.coordinates['s'] > 0:
        player.coordinates['s'] -= 1
    else:
        player.coordinates['n'] += 1

def update_east():
    if player.coordinates['w'] > 0:
        player.coordinates['w'] -= 1
    else:
        player.coordinates['e'] += 1

def update_south():
    if player.coordinates['n'] > 0:
        player.coordinates['n'] -= 1
    else:
        player.coordinates['s'] += 1

def update_west():
    if player.coordinates['e'] > 0:
        player.coordinates['e'] -= 1
    else:
        player.coordinates['w'] += 1

def update_coordinates(movement):
    if movement.lower() == 'n':
        return update_north()
    if movement.lower() == 'e':
        return update_east()
    if movement.lower() == 's':
        return update_south()
    if movement.lower() == 'w':
        return update_west()

def ask_for_action():
    current_room = game_map.get_room(player.str_coordinates())
    print(current_room.str_actions())
    action_decision = input('').split()

    while action_decision[0] not in current_room.actions:
        print(current_room.str_actions())
        action_decision = input('').split()

    return action_decision

def move(*args):
    current_room = game_map.get_room(player.str_coordinates())
    directions = current_room.next_rooms

    print("You can move to: {}. A direction alsjeblieft:".format(', '.join(directions)))
    direction = input('')

    while direction.lower() not in directions:
        print("{}. A direction alsjeblieft:".format(directions))
        direction = input('')

    update_coordinates(direction)

def take(*args):
    current_room = game_map.get_room(player.str_coordinates())
    items_types = list(map(str.lower, current_room.get_items_types()))
    items_names = list(map(str.lower, current_room.get_items_names()))

    separated_items_names = []

    for item_name in items_names:
        for word in item_name.split():
            separated_items_names.append(word)

    if args:
        arg_in_name = []
        arg_not_in_name = set()
        for arg in args:
            if arg in separated_items_names:
                arg_in_name.append(arg)
            else:
                arg_not_in_name.add(arg)

        print(arg_in_name, arg_not_in_name)

        if len(arg_not_in_name) > 0 and len(arg_in_name) > 0:
            for i in range(0, len(items_names)):
                if arg_in_name[0] in items_names[i]:
                    item_index = i
            print("Do you want to take the {}?".format(items_names[item_index]))

        if len(arg_not_in_name) == 0 and len(arg_in_name) > 0:
            asked_items = set()
            for i in range(0, len(items_names)):
                for name in arg_in_name:
                    if name in items_names[i]:
                        asked_items.add(items_names[i])
                        item_index = i

            if len(asked_items) > 1:
                print("Do you want to take the {}?".format(items_names[item_index]))
            else:
                player.inventory["albums"].append(current_room.items[item_index])
                player.get_inventory()

actions = {
    "move": move,
    "take": take,
    "inventory": player.get_inventory,
    "coordinates": player.get_coordinates
}

def main():

    while True:
        action = ask_for_action()
        if action[0] in actions:
            args = action[1:]
            if len(args):
                actions[action[0]](*args)
            else:
                actions[action[0]]()
        else:
            print("Sorry please, alsjeblieft ):")

main()
