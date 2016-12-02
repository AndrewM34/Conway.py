# A program to simulate Conway's Game of Life.

# 1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by over-population.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

from Canvas import *
from itertools import *

def grid(size, n, colour): # creates a nxn grid.
    i = 0
    while i < n + 1:
        create_line(10 + size*i, 10 , 10 + size*i,10 + (size*n), fill=colour)
        create_line(10, 10 + size*i, 10 + size*n, 10 + size*i, fill=colour)
        i += 1

def rectGrid(size, m, n): # creates an mxn grid.
    xEnd = m*size
    yEnd = n*size
    for i in range(m+1): # lines perp. to x-axis
        create_line(size*i,0,size*i,yEnd, fill="grey")
    for j in range(n+1): # lines perp. to y-axis
        create_line(0,size*j,xEnd,size*j, fill="grey")

def allCells(grid): # returns each 'point' on the plane
    tens = []
    cells = []
    i = 1
    while i < grid+2:
        tens.append(i*10)
        i += 1
    points = product(tens,tens)
    for point in points:
        cells.append(point)
    return cells

def drawSq(pos):    # takes the output from squarePos or a list: [x, y]
    create_rectangle(pos[0], pos[1], pos[0]+10, pos[1]+10, fill="black", tags = 'cell')

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
            neighbour = [x+(10*i),y-10]
            if neighbour not in aliveCells and neighbour not in neighbours:
                neighbours.append(neighbour)

        for j in range(-1,2):
            neighbour = [x+(10*j),y]
            if neighbour not in aliveCells and neighbour not in neighbours:
                neighbours.append(neighbour)

        for k in range(-1,2):
            neighbour = [x+(10*k),y+10]
            if neighbour not in aliveCells and neighbour not in neighbours:
                neighbours.append(neighbour)

    return neighbours

def key(str):
    if str == '1':
        return 1
    elif str == '2':
        return 2
    elif str == '3':
        return 3
    elif str == '4':
        return 4
    else:
        return False

def mouseClick(x, y, num):
    global start
    global click
    redraw = False
    click = num
    cellId = str(x) + ',' + str(y)
    cX = (x/10)*10
    cY = (y/10)*10

    if cX == 0 and cY == 0: # user clicked start button
        game(start)

    if num == 1 and cX != 0 and cY != 0:  # create square, left click
        if [cX,cY] not in start:
            print "click at:", x, y,", drawing at:", cX, cY
            start.append([cX,cY])
            # drawSq([(x/10)*10,(y/10)*10])
            create_rectangle(cX, cY, 10+cX, 10+cY, fill="black", tags="input")

    elif num == 3: # right click, delete cell CLEAN THIS function UP!
        print "click at:", x, y,", deleting square at:", cX, cY
        if [cX,cY] not in start:
            print "cell not already selected."
        elif [cX,cY] in start:
            start.remove([(x/10)*10,(y/10)*10])
            redraw = True
            delete( "all" )
            create_rectangle(0, 0, 10, 10, fill="red", tags = 'clickToStart')
            rectGrid(size, xMax/size, yMax/size)
            drawAll(start)

    else:
        print "starting"
        game(start)

def interrupt(x,y,num):
    if num == 1:
        complete() # if user clicks during game, stop

# def welcome(key):
#     choice = key
#     if choice == '1':
#         print "choice == 1"
#     elif choice == '2':
#         unset_keydown_handler(key)
#         set_mousedown_handler(mouseClick)
#     else:
#         print choice



##### function definitions for main game/rules #####

def sumNeighbours(sq, reflist):     # as tuples
    x = sq[0]
    y = sq[1]
    sum = 0

    for i in range(-1,2):
        if [x+(10*i),y-10] in reflist:
            sum += 1

    for j in range(-1,2):
        if [x+(10*j),y+10] in reflist:
            sum += 1

    for k in range(-1,2):
        if [x+(10*k),y] in reflist:
            sum += 1

    if [x,y] in reflist:
        sum = sum - 1

    return sum

def removeOutliers(listIn):
    for outlier in listIn:
        if outlier[0] <= 10 or outlier[0] >= 110:
            listIn.remove(outlier)
        if outlier[1] <= 10 or outlier[1] >= 110:
            listIn.remove(outlier)
    return listIn

def game( start ): #takes a list of starting cells
    unset_mousedown_handler(mouseClick)
    cells = start + []
    drawAll(cells)
    set_mousedown_handler(interrupt)
    while cells != []: # loops until there are no more cells
        allCells = allLocalCells(cells) + []

        cellsTemp = cells + []
        checkRev = cellsTemp + []

        for revivable in allCells:
            totalNeighbours = sumNeighbours(revivable, checkRev)
            # print revivable, "has", totalNeighbours, "neighbours"
            if totalNeighbours == 3:
                # print "revivable:", [revivable[0],revivable[1]]
                cellsTemp.append([revivable[0],revivable[1]])

        for dead in checkRev:
            toDie = sumNeighbours(dead, checkRev)
            if toDie < 2 or toDie > 3: # under or over population
                cellsTemp.remove(dead)

        wait( 0.1 )
        delete( 'all' )
        allCells = []
        cells = cellsTemp + []
        drawAll(cells)
    complete()

###################################################################
xMax, yMax = 1200, 900
size = 10 #!!! DO NOT CHANGE THIS VARIABLE, too much hardcode !!!#
rectGrid(size, xMax/size, yMax/size)
set_size( xMax, yMax)
click = 1
keypress = False
choiceText = "[1] - Choose from a preset \n[2] - Create an arrangement"

########## Built-in shapes for easy reference ##########
block = [[50,50],[60,50],[50,40],[60,40]]
blinker = [[30,30],[30,40],[30,50]]
glider = [[30,20],[40,30],[20,40],[30,40],[40,40]]
gosper = [[20,60],[20,70],[30,60],[30,70],[120,60],[120,70],[120,80],[130,50],[130,90],[140,40],[140,100],[150,40],[150,100],[160,70],[170,50],[170,90],[180,60],[180,70],[180,80],[190,70],[220,40],[220,50],[220,60],[230,40],[230,50],[230,60],[240,30],[240,70],[260,20],[260,30],[260,70],[260,80],[360,40],[360,50],[370,40],[370,50]]
start = []

set_mousedown_handler(mouseClick)
create_rectangle(0, 0, 10, 10, fill="red", tags = 'clickToStart')
create_text(75,20, text="click red square to start")

# welcome = create_text(100,100, font="Hack", text="Game of Life Simulator")
# dialogue = create_text(100,130, font="Hack", text = choiceText)
# set_keydown_handler(welcome)
run()
# unset_mousedown_handler( mouseClick )

game(gosper)
complete()
