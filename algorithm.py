from queue import PriorityQueue
import queue

class Node:

    def __init__(self, t,ftotal,gcost,heu):
        self.kind = t
        self.f = ftotal
        self.g = gcost
        self.h = heu

        self.color = (0,0,0)

    def canTraverse(self):
        return False if self.kind == "wall" else True

    def updateNeighbors(self, grid):
        self.neighbors = []

def h(start,end):
    x1, y1 = start
    x2,y2 = end
    return abs(x1-x2) + abs(y1-y2)

def astar(grid, startpos, goal):
    # fill in heuristic values

    for x in range(20):
        for y in range(20):
            grid[x][y].h = h((x,y),goal)

    openList = queue.PriorityQueue()
    closedList  = []




def main():
    grid = [[Node("open", float('inf'), float('inf'), float('inf')) for x in range(20)] for y in range(20)]
    startpos = 0,0
    endpos = 15,15


    for x in range(10):
        grid[x][5].kind = "wall"

    astar(grid, startpos, endpos)


main()