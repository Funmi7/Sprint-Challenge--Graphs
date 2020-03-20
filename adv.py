from room import Room
from player import Player
from world import World
from util import Queue

import random
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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def explore(player, moves_cue):
    q = Queue()
    visited = set()
    q.enqueue([player.current_room.id])
    while q.size() > 0:
        path = q.dequeue()
        last_room = path[-1]
        if last_room not in visited:
            visited.add(last_room)
            for exits in graph[last_room]:
                if graph[last_room][exits] == "?":
                    return path
                else:
                    lost = list(path)
                    lost.append(graph[last_room][exits])
                    q.enqueue(lost)
    return []


def q_moves(player, moves_q):
    current_exits = graph[player.current_room.id]
    untried_exits = []
    for direction in current_exits:
        if current_exits[direction] == "?":
            untried_exits.append(direction)
    if len(untried_exits) == 0:
        unexplored = explore(player, moves_q)
        room_id = player.current_room.id
        for next_dir in unexplored:
            for direction in graph[room_id]:
                if graph[room_id][direction] == next_dir:
                    moves_q.enqueue(direction)
                    room_id = next_dir
                    break
    else:
        moves_q.enqueue(untried_exits[random.randint(0, len(untried_exits) - 1)])


optimum_path = []
player = Player(world.starting_room)
graph = {}

def traverse_map(optimum_path, player, graph):

    fresh_room = {}
    for direction in player.current_room.get_exits():
        fresh_room[direction] = "?"
    graph[world.starting_room.id] = fresh_room

    moves_q = Queue()
    total_moves = []
    q_moves(player, moves_q)

    reverse_compass = {"n": "s", "s": "n", "e": "w", "w": "e"}

    while moves_q.size() > 0:
        starting = player.current_room.id
        next_dir = moves_q.dequeue()
        player.travel(next_dir)
        total_moves.append(next_dir)
        end = player.current_room.id
        graph[starting][next_dir] = end
        if end not in graph:
            graph[end] = {}
            for exits in player.current_room.get_exits():
                graph[end][exits] = "?"
        graph[end][reverse_compass[next_dir]] = starting
        if moves_q.size() == 0:
            q_moves(player, moves_q)
   
    optimum_path = total_moves
    return optimum_path 

traversal_path = traverse_map(optimum_path, player, graph)

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
