from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Stack, Queue
from collections import defaultdict
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
opposite = {
    'n': 's', 
    'e': 'w', 
    's': 'n', 
    'w': 'e'
}
# player.current_room.id
# player.current_room.get_exits()
# player.travel(direction)

# when moving to another room (going south for example)
# set previous room (south) to the id of current room
# set current room oposite direction (north) to id of previous room

def projected_path(starting_room, already_visited=set()):
    visited = set()
    # update visited
    for room in already_visited: visited.add(room)
    # hold path
    path = []
    def add_to_path(room, back=None):
        # add room to visited
        print(path)
        visited.add(room)
        # get all room exits
        exits = room.get_exits()
        # for each exit
        for direction in exits:
            # if the room in that direction is not visited
            if room.get_room_in_direction(direction) not in visited:
                # add the direction to the path
                path.append(direction)
                # recursively add all the rooms in the same direction, while sending the way back
                add_to_path(room.get_room_in_direction(direction), opposite[direction])
        # if a way back exists, add it to the path
        if back: path.append(back)
    # start running at starting room
    add_to_path(starting_room)
    # return projected path
    return path

def create_path(starting_room, visited=set()):
    # hold the path
    path = []
    def add_to_path(room, back=None):
        # add room to visited
        visited.add(room)
        # get all room exits
        exits = room.get_exits()
        # hold all path projections
        path_lengths = {}
        # for each exit
        for direction in exits:
            # find projected path in that direction
            path_lengths[direction] = len(projected_path(room.get_room_in_direction(direction), visited))
        # hold the traverse order of the paths
        traverse_order = []
        # for each direction as projected path sorted by length of path
        for direction, _ in sorted(path_lengths.items(), key = lambda x: x[1]): 
            # add the direction to the traverse order
            traverse_order.append(direction)
        # for each direction in the traverse order
        for direction in traverse_order:
            # if the room in that direction was not visited
            if room.get_room_in_direction(direction) not in visited:
                # add direction to the path
                path.append(direction)
                # recursively add all the rooms in the same direction, while sending the way back
                add_to_path(room.get_room_in_direction(direction), opposite[direction])
        # if we've reached all rooms at least once, stop
        if len(visited) == len(world.rooms): return
        # else, go back and append to path
        elif back: path.append(back)
    # start running at starting room
    add_to_path(starting_room)
    # return path
    return path

traversal_path = create_path(world.starting_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
