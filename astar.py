import sys
import pygame
import time

pygame.init()

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "walls": (117, 117, 110),
    "startsquare": (45, 201, 55),
    "endsquare": (66, 135, 245),
    "buttonOutline": (75, 103, 148),
    "mainpath": (235, 64, 52),
    "pathedge": (165, 24, 217),
    "finalpath": (0, 100, 100)
}  # colors of elements in program


class Node():

    def __init__(self, row, col, endpos):
        self.f = float('inf')
        self.g = float('inf')
        self.y = row
        self.x = col
        self.kind = "open"
        self.color = colors["white"]
        # manhattan distance formula to find pos
        self.h = abs(endpos[1] - self.y) + abs(endpos[0] - self.x)

    def neighbors(self):  # row is y, col is x | grid is 49x31
        list_n = []

        if self.y - 1 >= 0:
            if grid[self.x][self.y-1].isOpen():  # ? square to the left
                list_n.append(grid[self.x][self.y-1])

        if self.y + 1 < 32:
            if grid[self.x][self.y+1].isOpen():  # ? square to the right
                list_n.append(grid[self.x][self.y+1])

        if self.x - 1 >= 0:
            if grid[self.x-1][self.y].isOpen():  # ? square below
                list_n.append(grid[self.x-1][self.y])

        if self.x + 1 < 50:
            if grid[self.x+1][self.y].isOpen():  # ? square above
                list_n.append(grid[self.x+1][self.y])

        return list_n

    def updateType(self, newtype):
        self.kind = newtype

        if newtype == "open":
            self.color == colors["white"]
        elif newtype == "wall":
            self.color == colors["walls"]
        elif newtype == "start":
            self.color == colors["startsquare"]
        elif newtype == "end":
            self.color == colors["endsquare"]
        elif newtype == "mainpath":
            self.color == colors["mainpath"]
        elif newtype == "pathedge":
            self.color == colors["pathedge"]
        elif newtype == "finalpath":
            self.color == colors["finalpath"]

    def updateH(self, endpos):
        self.h = abs(endpos[1] - self.y) + abs(endpos[0] - self.x)

    def isOpen(self):
        return False if self.kind == "wall" else True

    def reset(self):
        self.kind = "open"
        self.color = colors["white"]
        self.f = float('inf')
        self.g = float('inf')
        self.h = abs(endpos[1] - self.y) + abs(endpos[0] - self.x)


window_dimensions = 1500, 800  # set window dimensions

#! render fonts and texts for buttons
smallfont = pygame.font.SysFont("ubuntumono", 25)
resetButtonText = smallfont.render('Reset Grid', True, colors["black"])
chooseAlgoTexts = [smallfont.render(
    "A*", True, colors["black"]), smallfont.render("Dijkstra", True, colors["black"])]
findRouteText = smallfont.render("Calculate Route", True, colors["black"])
noRouteFoundText = smallfont.render("No route", True, colors["black"])


surface = pygame.display.set_mode(window_dimensions)  # make 1500x800 window
pygame.display.set_caption("Visualizing A*")  # set window title
surface.fill(colors["white"])  # white background


# define default startpos and endpos
startpos = 5, 5
endpos = 40, 25

grid = [[Node(x, y, endpos) for x in range(32)] for y in range(50)]


# ! initialize default starting position
grid[startpos[0]][startpos[1]].updateType("start")
# ! initalize default ending position
grid[endpos[0]][endpos[1]].updateType("end")

# draw other UI elements once, statically
pygame.draw.rect(surface, colors["buttonOutline"],
                 pygame.Rect(1315, 50, 150, 25))
pygame.draw.rect(surface, colors["buttonOutline"],
                 pygame.Rect(1315, 100, 125, 25))
pygame.draw.rect(surface, colors["buttonOutline"],
                 pygame.Rect(1270, 700, 205, 25))

surface.blit(resetButtonText, (1320, 50))
surface.blit(chooseAlgoTexts[1], (1320, 100))
surface.blit(findRouteText, (1275, 700))


def drawGrid():
    blockSize = 25  # set the size of each grid square
    drawflag = False  # controls whether a filled square needs to be drawn

    for x in range(0, 50):
        for y in range(0, 32):
            rect = pygame.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pygame.draw.rect(surface, colors["black"], rect, 1)

            if grid[x][y].kind == "open":
                squareColor = colors["black"]
                pygame.draw.rect(surface, colors["white"], pygame.Rect(
                    x*blockSize+1, y*blockSize+1, blockSize-2, blockSize-2))
                drawflag = False
            elif grid[x][y].kind == "wall":
                squareColor = colors["walls"]
                drawflag = True
            elif grid[x][y].kind == "start":
                squareColor = colors["startsquare"]
                drawflag = True
            elif grid[x][y].kind == "end":
                squareColor = colors["endsquare"]
                drawflag = True
            elif grid[x][y].kind == "mainpath":
                squareColor = colors["mainpath"]
                drawflag = True
            elif grid[x][y].kind == "pathedge":
                squareColor = colors["pathedge"]
                drawFlag = True
            elif grid[x][y].kind == "finalpath":
                squareColor = colors["finalpath"]
                drawflag = True
            if drawflag:
                pygame.draw.rect(surface, squareColor, pygame.Rect(
                    x*blockSize+1, y*blockSize+1, blockSize-2, blockSize-2))  # draw rect to fill in grid square
    pygame.display.update()


def mousePressed(pos, buttons):  # ! handles mousepressed events
    if pos[0] < 1250:
        gridxy = int(pos[0]/25), int(pos[1]/25)
        if gridxy == startpos or gridxy == endpos:
            pass  # ! make start and end positions moveable soon
            # for now, prevent player from removing start/end position markers
        elif buttons[2]:
            grid[gridxy[0]][gridxy[1]].updateType("open")
        elif buttons[0]:
            grid[gridxy[0]][gridxy[1]].updateType("wall")

    elif pos[0] > 1315 and pos[0] < 1465 and pos[1] > 50 and pos[1] < 75:
        for x in range(0, 50):
            for y in range(0, 32):
                grid[x][y].reset()
        grid[startpos[0]][startpos[1]].updateType("start")
        grid[endpos[0]][endpos[1]].updateType("end")


def reconstruct_path(cameFrom, current):
    totalPath = [current]

    while current in cameFrom.keys():
        current = cameFrom[current]
        totalPath.insert(0, current)

    totalPath.reverse()

    for item in totalPath[1:len(totalPath)-1]:
        grid[item.x][item.y].updateType("finalpath")
        drawGrid()
        time.sleep(0.015)


def astar(grid, start, end):
    #! update h values for the entire grid

    for x in range(50):  # ! update heuristic values for entire grid
        for y in range(32):
            grid[x][y].updateH(end)

    openSet = []
    # ! add start square to open set to review
    openSet.append(grid[start[0]][start[1]])

    cameFrom = {}

    grid[startpos[0]][startpos[1]].g = 0

    grid[startpos[0]][startpos[1]].f = grid[startpos[0]][startpos[1]].h

    while openSet:
        temp = float('inf')
        current = 0
        for item in openSet:
            if item.f < temp:
                temp = item.f
                current = item
        if current.x == end[0] and current.y == end[1]:
            return reconstruct_path(cameFrom, current)

        if current.x == start[0] and current.y == start[1]:
            pass
        else:
            grid[current.x][current.y].updateType("mainpath")
        drawGrid()
        time.sleep(0.005)
        openSet.remove(current)

        neighbors = current.neighbors()

        if not neighbors:
            return "failure"

        for neighbor in neighbors:
            tentativeG = current.g + 1

            if tentativeG < neighbor.g:
                cameFrom[neighbor] = current
                neighbor.g = tentativeG
                neighbor.f = tentativeG + neighbor.h

                if neighbor not in openSet:
                    openSet.append(neighbor)

    return "pathfinding failed"


def main():
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # check for exit
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                temppos = pygame.mouse.get_pos()
                if temppos[0] > 1270 and temppos[0] < 1475 and temppos[1] > 700 and temppos[1] < 725:
                    astar(grid, startpos, endpos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    astar(grid, startpos, endpos)

            if True in pygame.mouse.get_pressed():
                mousePressed(pygame.mouse.get_pos(),
                             pygame.mouse.get_pressed())

        drawGrid()
        pygame.display.update()  # update display after new grid has been drawn


if __name__ == "__main__":
    main()