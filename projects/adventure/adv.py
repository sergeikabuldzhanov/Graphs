from room import Room
from player import Player
from world import World

import random
from collections import deque
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
directions_map = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

visited = {}
current_room = world.starting_room
room_stack = deque()
# room_stack.append()
room_id_path = []
# until we have visited all rooms
while len(visited) < len(world.rooms):
    # traverse the graph depth fisrt
    # every time we change current node, add it to path
    # if the current node is not visited, mark it as visited
    if current_room.id not in visited:
        # set the connections to None, as we don't know the room id's yet
        visited[current_room.id] = dict.fromkeys(
            current_room.get_exits(), None)
        room_id_path.append(current_room.id)
    # find unvisited neighbors
    unvisited = [direction for direction in visited[current_room.id]
                 if visited[current_room.id][direction] == None]
    if len(unvisited):
        room_stack.append(current_room)
        # move_direction = unvisited[0]
        move_direction = random.choice(unvisited)
        next_room = current_room.get_room_in_direction(move_direction)
        visited[current_room.id][move_direction] = next_room.id
        if next_room.id not in visited:
            visited[next_room.id] = dict.fromkeys(
                next_room.get_exits(), None)
            visited[next_room.id][directions_map[move_direction]] = current_room.id
        room_id_path.append(next_room.id)
        traversal_path.append(move_direction)
        current_room = next_room
    else:
        previous_room = current_room
        current_room = room_stack.pop()
        direction, = [d for d in visited[previous_room.id]
                      if visited[previous_room.id][d] == current_room.id]
        traversal_path.append(direction)
        room_id_path.append(current_room.id)

# world.print_rooms()
# print(room_id_path)
# print(traversal_path)
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

"""
#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
"""
