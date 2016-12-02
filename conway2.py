# implementation of Conway's game of life in python
# Andrew Mcnab, 12/12/2015
#
# The game works by the following 4 rules:
# 1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by over-population.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

from Canvas import *
from itertools import *

def rectGrid(size, m, n): # creates an mxn grid.
    xEnd = m*size
    yEnd = n*size
    for i in range(m+1): # lines perp. to x-axis
        create_line(size*i,0,size*i,yEnd, fill="grey")
    for j in range(n+1): # lines perp. to y-axis
        create_line(0,size*j,xEnd,size*j, fill="grey")

def drawSq(pos):    # takes the output from squarePos or a list: [x, y]
    create_rectangle(pos[0], pos[1], pos[0]+size, pos[1]+size, fill="black", tags = 'cell')

def drawAll(inp):
    i = 0
    for draw in inp:
        drawSq(draw)

def allLocalCells(aliveCells): # returns a list of all neighbouring cells
    neighbours = []
    for alive in aliveCells:
        x = alive[0]
        y = alive[1]

        for i in range(-1,2):
            neighbour = [x+(size*i),y-size]
            if neighbour not in aliveCells and neighbour not in neighbours:
                neighbours.append(neighbour)

        for j in range(-1,2):
            neighbour = [x+(size*j),y]
            if neighbour not in aliveCells and neighbour not in neighbours:
                neighbours.append(neighbour)

        for k in range(-1,2):
            neighbour = [x+(size*k),y+size]
            if neighbour not in aliveCells and neighbour not in neighbours:
                neighbours.append(neighbour)

    return neighbours

def sumNeighbours(sq, reflist):     # as tuples
    x = sq[0]
    y = sq[1]
    sum = 0

    for i in range(-1,2):
        if [x+(size*i),y-size] in reflist:
            sum += 1

    for j in range(-1,2):
        if [x+(size*j),y+size] in reflist:
            sum += 1

    for k in range(-1,2):
        if [x+(size*k),y] in reflist:
            sum += 1

    if [x,y] in reflist:
        sum = sum - 1

    return sum

######## define mouse handler for custom starts ########
def mouseClick(x, y, num):
    global start
    click = num
    cellId = str(x) + ',' + str(y)
    cX = (x/size)*size
    cY = (y/size)*size

    if cX == 0 and cY == 0: # user clicked start button
        game(start)

    if num == 1 and cX != 0 and cY != 0:  # create square, left click
        if [cX,cY] not in start:
            print "click at:", x, y,", drawing at:", cX, cY
            start.append([cX,cY])
            create_rectangle(cX, cY, size+cX, size+cY, fill="black", tags="input")

    elif num == 3: # right click, delete cell
        print "click at:", x, y,", deleting square at:", cX, cY
        if [cX,cY] not in start:
            print "cell not already selected."
        elif [cX,cY] in start:
            try:
                start.remove([(x/size)*size,(y/size)*size])
            except:
                print "Error in deleting cell - does not exist."
            delete('all')
            # create_rectangle(0, 0, size, size, fill="red", tags = 'clickToStart')
            rectGrid(size, xMax/size, yMax/size)
            drawAll(start)

    else:
        print "starting"
        game(start)

################## main game function ##################

def game( start ): #takes a list of starting cells
    cells = start + []
    drawAll(cells)

    while cells != []:
        allCells = allLocalCells(cells) + []
        cellsTemp = cells + []
        checkRev = cellsTemp + []

        for revivable in allCells: # exactly 3 neighbours - revive
            totalNeighbours = sumNeighbours(revivable, checkRev)
            if totalNeighbours == 3:
                cellsTemp.append([revivable[0],revivable[1]])

        for dead in checkRev:
            toDie = sumNeighbours(dead, checkRev)
            if toDie < 2 or toDie > 3: # under or over population
                cellsTemp.remove(dead)

        allCells = []
        cells = cellsTemp + []
        delete('all')
        drawAll(cells)
        wait( 0.1 )

    create_text(600, 300, text='All cells died. Click to end.')

    complete()

########################################################
############### variables for the screen ###############
xMax, yMax = 1200, 900
size = 10

############## draw grid, set window size ##############
rectGrid(size, xMax/size, yMax/size)
set_size(xMax, yMax)

########## Built-in shapes for easy reference ##########
block = [[50,50],[60,50],[50,40],[60,40]]
blinker = [[30,30],[30,40],[30,50]]
glider = [[30,20],[40,30],[20,40],[30,40],[40,40]]
gosper = [[20,60],[20,70],[30,60],[30,70],[120,60],[120,70],[120,80],[130,50],[130,90],[140,40],[140,100],[150,40],[150,100],[160,70],[170,50],[170,90],[180,60],[180,70],[180,80],[190,70],[220,40],[220,50],[220,60],[230,40],[230,50],[230,60],[240,30],[240,70],[260,20],[260,30],[260,70],[260,80],[360,40],[360,50],[370,40],[370,50]]
start = []

################### run in draw mode ###################
# set_mousedown_handler(mouseClick)
# run()

################# run in pre-made mode #################
game(gosper)

################# call complete to end #################
complete()
