from puzz import EightPuzzleBoard
import sys
from collections import OrderedDict

EXPANDED = 0
FRONTIER = 1
PATHCOST = 0


def bfs(start, goal):
    global FRONTIER
    frontier = []
    explored = set()  # Eightpuzzboard object
    frontier.append([["start", start]])  # List of path of tuples
    while not len(frontier) == 0:
        path = frontier.pop(0)
        node = path[-1][-1]
        explored.add(node)
        for each in expand(node):
            if not inFrontier(each[1], frontier) and each[1] not in explored:
                newPath = path[:]
                newPath.append(each)
                if each[1] == goal:
                    return newPath
                frontier.append(newPath)
                FRONTIER += 1
    return None


def ucost(start, goal):
    global FRONTIER
    frontier = OrderedDict()
    explored = set()
    frontier[start] = [["start", start]]
    while not len(frontier) == 0:
        frontier = OrderedDict(
            sorted(frontier.items(), key=lambda each: len(each[1])))
        node, path = frontier.popitem(last=False)
        explored.add(node)
        if node == goal:
            return path
        for each in expand(node):
            newPath = path[:]
            newPath.append(each)
            if each[1] not in frontier and each[1] not in explored:
                frontier[each[1]] = newPath
                FRONTIER += 1
            elif each[1] in frontier and len(frontier[each[1]]) > len(newPath):
                frontier[each[1]] = newPath
                FRONTIER += 1
    return None


def greedyCount(start, goal):
    global FRONTIER
    frontier = OrderedDict()
    explored = set()
    frontier[start] = [[["start", start]], misplaced_count(start, goal)]
    while not len(frontier) == 0:
        frontier = OrderedDict(sorted(frontier.items(), key=lambda each: each[1][1]))
        node, pair = frontier.popitem(last=False)
        path = pair[0]
        explored.add(node)
        if node == goal:
            return path
        for each in expand(node):
            newPath = path[:]
            newPath.append(each)
            misplaced = misplaced_count(each[1], goal)
            if each[1] not in frontier and each[1] not in explored:
                frontier[each[1]] = [newPath, misplaced]
                FRONTIER += 1
            elif each[1] in frontier and frontier[each[1]][1] > misplaced:
                frontier[each[1]] = [newPath, misplaced]
                FRONTIER += 1
    return None


def greedyManhat(start, goal):
    
    return ["start", start]


def astarCount(start, goal):
    global FRONTIER
    frontier = OrderedDict()
    explored = set()
    frontier[start] = [[["start", start]], misplaced_count(start, goal)]
    while not len(frontier) == 0:
        frontier = OrderedDict(sorted(frontier.items(),key=lambda each: each[1][1]))
        node, pair = frontier.popitem(last=False)
        path = pair[0]
        explored.add(node)
        if node == goal:
            return path
        for each in expand(node):
            newPath = path[:]
            newPath.append(each)
            f = len(newPath) + misplaced_count(each[1], goal)
            if each[1] not in frontier and each[1] not in explored:
                frontier[each[1]] = [newPath, f]
                FRONTIER += 1
            elif each[1] in frontier and frontier[each[1]][1] > f:
                frontier[each[1]] = [newPath, f]
                FRONTIER += 1
    return None


def astarManhat(start, goal):
    return 0

# Helper Functions


def expand(node: EightPuzzleBoard):
    global EXPANDED
    expansion = node.successors()
    returnExapnsion = []
    EXPANDED += 1
    for key in expansion:
        if expansion[key] is not None:
            returnExapnsion.append([key, expansion[key]])
    return returnExapnsion


def inFrontier(node, frontier):
    for each in frontier:
        if node == each[-1][-1]:
            return True
    return False


def misplaced_count(node, goal):
    counter = 0
    nodestr = str(node)
    goalstr = str(goal)
    for i in range(0, len(nodestr)):
        if not nodestr[i] == goalstr[i]:
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
    output(path)


if __name__ == "__main__":
    mod = sys.argv[1]
    start = sys.argv[2]
    goal = sys.argv[3]
    run(mod, start, goal)
