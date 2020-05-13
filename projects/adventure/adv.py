from room import Room
from player import Player
from world import World

import random
from collections import deque, defaultdict
import heapq
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
while len(visited) is not len(world.rooms):
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
        move_direction = unvisited[0]
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

graph = [[value for value in v.values() if value is not None]
         for k, v in sorted(visited.items(), key=lambda x: x[0])]


def bfs(starting_vertex, destination_vertex):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    visited = set()
    visited.add(starting_vertex)
    paths = deque()
    paths.appendleft([starting_vertex])
    # print(starting_vertex)
    # store a queue of paths
    while len(paths):
        path = paths.pop()
        node = path[-1]
        # if the path ends with destination vertex, that the path we need, bfs ensures it's the shortest
        if node == destination_vertex:
            return path
        # else, look at all the neghbours, and add new paths to the queue
        else:
            for adjacent in graph[node]:
                if adjacent not in visited:
                    visited.add(node)
                    new_path = path+[adjacent]
                    paths.appendleft(new_path)


shortest_paths = [[bfs(starting_node, target_node)
                   for target_node in range(len(graph))]for starting_node in range(len(graph))]
# print(shortest_paths)

def bfs_all_paths(graph, starting_vertex):
    min_path_len = 99999999999
    min_path = []
    paths = deque()
    # for every path we store the path and nodes visited so far
    paths.appendleft(([starting_vertex], set([starting_vertex])))
    # store a queue of paths
    while len(paths):
        path, visited = paths.pop()
        # last node in a path is the one we are looking at
        node = path[-1]
        # if the path has visited all the nodes, done
        if len(visited) == len(graph):
            if len(path)< min_path_len:
                min_path = path
                min_path_len = len(path)
                # print(min_path, min_path_len)
            # return path
        else:
            # else, look at all the neghbours for the current node
            unvisited = [n for n in graph[node] if n not in visited]
            if unvisited:
                for adjacent in unvisited:
                    # if there are unvisited ones, add them to path and new path to queue
                    new_path = path+[adjacent]
                    new_visited = visited.copy()
                    new_visited.add(adjacent)
                    paths.appendleft((new_path, new_visited))
            else:
                # else if there are no unvisited nodes, backtrack until we find a node with
                # unvisited neighbours 
                # add the backtracking path to path
                for node_id in reversed(path):
                    unvisited = [n for n in graph[node_id] if n not in visited]
                    if unvisited:
                        path_back = shortest_paths[node][node_id][1::]
                        for adjacent in unvisited:
                            # if there are unvisited ones, add them to path and new path to queue
                            new_path = path+path_back+[adjacent]
                            new_visited = visited.copy()
                            new_visited.add(adjacent)
                            paths.appendleft((new_path, new_visited))
    return min_path, min_path_len-1

world.print_rooms()
print("bfs smart",bfs_all_paths(graph, 0))
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
