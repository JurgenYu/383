from heapq import heappop
from heapq import heappush
import itertools

def ucost(start, goal):
    def add_task(task, path):
        priority = len(path)
        if task in entry_finder:
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = path
        heappush(frontier, entry)

    def remove_task(task):
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task():
        while frontier:
            priority, count, task = heappop(frontier)
            if task is not REMOVED:
                p = entry_finder[task]
                del entry_finder[task]
                return [task, p]
        raise KeyError('pop from an empty priority queue')
    global FRONTIER
    global EXPANDED
    counter = itertools.count()
    REMOVED = '<removed-task>'
    goalstr = str(goal)
    frontier = []
    entry_finder = {}
    explored = set()
    add_task(str(start), [tuple(["start", start])])
    while not len(frontier) == 0:
        if EXPANDED >= 100000:
            return None
        node, path = pop_task()
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
            if newnode not in entry_finder and newnode not in explored:
                add_task(newnode, newPath)
                FRONTIER += 1
            elif newnode in entry_finder and len(entry_finder[newnode]) > len(newPath):
                add_task(newnode, newPath)
                FRONTIER += 1
    return None