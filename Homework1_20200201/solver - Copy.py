from puzz import EightPuzzleBoard
import sys
from collections import OrderedDict
import heapq

EXPANDED = 0
FRONTIER = 1
PATHCOST = 0


def bfs(start, goal):
    global EXPANDED
    global FRONTIER
    goalstr = str(goal)
    frontier = OrderedDict()
    explored = set()  # Eightpuzzboard object
    frontier[str(start)] = [tuple(["start", start])]  # List of path of tuples
    while not len(frontier) == 0:
        node, path = frontier.popitem(last=False)
        explored.add(node)
        EXPANDED += 1
        for each in EightPuzzleBoard(node).successors().items():
            if each[1] is None:
                continue
            newnode = str(each[1])
            newPath = path[:]
            newPath.append(each)
            if newnode not in frontier and newnode not in explored:
                if newnode == goalstr:
                    return newPath
                frontier[newnode] = newPath
                FRONTIER += 1
    return None

def ucost(start, goal):
    global FRONTIER
    global EXPANDED
    goalstr = str(goal)
    frontier = OrderedDict()
    explored = set()
    frontier[str(start)] = [tuple(["start", start])]
    while not len(frontier) == 0:
        if EXPANDED >= 100000:
            return None
        print("new cycle")
        frontier = OrderedDict(
            sorted(frontier.items(), key=lambda each: len(each[1])))
        print("sorted")
        node, path = frontier.popitem(last=False)
        print("poped")
        explored.add(node)
        if node == goalstr:
            return path
        EXPANDED += 1
        print(EXPANDED)
        for each in EightPuzzleBoard(node).successors().items():
            if each[1] is None:
                continue
            newnode = str(each[1])
            newPath = path[:]
            newPath.append(each)
            if newnode not in frontier and newnode not in explored:
                frontier[newnode] = newPath
                FRONTIER += 1
            elif newnode in frontier and len(frontier[newnode]) > len(newPath):
                frontier[newnode] = newPath
                FRONTIER += 1
    return None


def greedyCount(start, goal):
    global FRONTIER
    global EXPANDED
    goalstr = str(goal)
    frontier = OrderedDict()
    explored = set()
    frontier[str(start)] = [[tuple(["start", start])], misplaced_count(start, goal)]
    while not len(frontier) == 0:
        frontier = OrderedDict(
            sorted(frontier.items(), key=lambda each: each[1][1]))
        node, pair = frontier.popitem(last=False)
        path = pair[0]
        explored.add(node)
        if node == goalstr:
            return path
        EXPANDED += 1
        for each in EightPuzzleBoard(node).successors().items():
            if each[1] is None:
                continue
            newnode = str(each[1])
            newPath = path[:]
            newPath.append(each)
            misplaced = misplaced_count(each[1], goal)
            if newnode not in frontier and newnode not in explored:
                frontier[newnode] = [newPath, misplaced]
                FRONTIER += 1
            elif newnode in frontier and frontier[newnode][1] > misplaced:
                frontier[newnode] = [newPath, misplaced]
                FRONTIER += 1
    return None


def greedyManhat(start, goal):
    global FRONTIER
    global EXPANDED
    goalstr = str(goal)
    frontier = OrderedDict()
    explored = set()
    frontier[str(start)] = [[tuple(["start", start])], manhattan(start, goal)]
    while not len(frontier) == 0:
        frontier = OrderedDict(
            sorted(frontier.items(), key=lambda each: each[1][1]))
        node, pair = frontier.popitem(last=False)
        path = pair[0]
        explored.add(node)
        if node == goalstr:
            return path
        EXPANDED += 1
        for each in EightPuzzleBoard(node).successors().items():
            if each[1] is None:
                continue
            newnode = str(each[1])
            newPath = path[:]
            newPath.append(each)
            misplaced = manhattan(each[1], goal)
            if newnode not in frontier and newnode not in explored:
                frontier[newnode] = [newPath, misplaced]
                FRONTIER += 1
            elif newnode in frontier and frontier[newnode][1] > misplaced:
                frontier[newnode] = [newPath, misplaced]
                FRONTIER += 1
    return None


def astarCount(start, goal):
    global FRONTIER
    global EXPANDED
    goalstr = str(goal)
    frontier = OrderedDict()
    explored = set()
    frontier[str(start)] = [[tuple(["start", start])], misplaced_count(start, goal)]
    while not len(frontier) == 0:
        frontier = OrderedDict(
            sorted(frontier.items(), key=lambda each: each[1][1]))
        node, pair = frontier.popitem(last=False)
        path = pair[0]
        explored.add(node)
        if node == goalstr:
            return path
        EXPANDED += 1
        for each in EightPuzzleBoard(node).successors().items():
            if each[1] is None:
                continue
            newnode = str(each[1])
            newPath = path[:]
            newPath.append(each)
            f = len(newPath) + misplaced_count(each[1], goal)
            if newnode not in frontier and newnode not in explored:
                frontier[newnode] = [newPath, f]
                FRONTIER += 1
            elif newnode in frontier and frontier[newnode][1] > f:
                frontier[newnode] = [newPath, f]
                FRONTIER += 1
    return None


def astarManhat(start, goal):
    global FRONTIER
    global EXPANDED
    goalstr = str(goal)
    frontier = OrderedDict()
    explored = set()
    frontier[str(start)] = [[tuple(["start", start])], manhattan(start, goal)]
    while not len(frontier) == 0:
        frontier = OrderedDict(
            sorted(frontier.items(), key=lambda each: each[1][1]))
        node, pair = frontier.popitem(last=False)
        path = pair[0]
        explored.add(node)
        if node == goalstr:
            return path
        EXPANDED += 1
        for each in EightPuzzleBoard(node).successors().items():
            if each[1] is None:
                continue
            newnode = str(each[1])
            newPath = path[:]
            newPath.append(each)
            f = len(newPath) + manhattan(each[1], goal)
            if newnode not in frontier and newnode not in explored:
                frontier[newnode] = [newPath, f]
                FRONTIER += 1
            elif newnode in frontier and frontier[newnode][1] > f:
                frontier[newnode] = [newPath, f]
                FRONTIER += 1
    return None

# Helper Functions


def manhattan(node, goal):
    nodestr = str(node)
    goalstr = str(goal)
    d = 0
    for i in range(0, len(nodestr)):
        if nodestr[i] == '0':
            continue
        else:
            nx = i % 3
            ny = 2 - int(i / 3)
            ig = goalstr.find(nodestr[i])
            gx = ig % 3
            gy = 2 - int(ig / 3)
            d += abs(gx - nx) + abs(gy-ny)
    return d


def misplaced_count(node, goal):
    counter = 0
    nodestr = str(node)
    goalstr = str(goal)
    for i in range(0, len(nodestr)):
        if nodestr[i] == '0':
            continue
        elif not nodestr[i] == goalstr[i]:
            counter += 1
    return counter


def output(path):
    global PATHCOST
    if path == None:
        if EXPANDED > 100000:
            print("Timed out")
        else:
            print("No Solution")
    else:
        for each in path:
            print(each[0] + "\t" + str(each[1]))
            PATHCOST += 1
        print("path cost:\t" + str(PATHCOST - 1))
        print("frontier:\t" + str(FRONTIER))
        print("expanded\t" + str(EXPANDED))


def run(mod, start, goal):
    start = EightPuzzleBoard(start)
    goal = EightPuzzleBoard(goal)
    if start == goal:
        output([["start", start]])
    elif mod == "bfs":
        path = bfs(start, goal)
    elif mod == "ucost":
        path = ucost(start, goal)
    elif mod == "greedy-count":
        path = greedyCount(start, goal)
    elif mod == "greedy-manhat":
        path = greedyManhat(start, goal)
    elif mod == "astar-count":
        path = astarCount(start, goal)
    elif mod == "astar-manhat":
        path = astarManhat(start, goal)
    else:
        print("Incorrect mode")
        path = None
    output(path)


if __name__ == "__main__":
    mod = sys.argv[1]
    start = sys.argv[2]
    goal = sys.argv[3]
    run(mod, start, goal)
