
from random import choice
import sys

from com.nineteengiraffes.Cell import Cell
from com.nineteengiraffes.Wall import Wall


def main():
    
    cells = blank_cells(2, 1, 2)
    walls = blank_walls(2, 1, 2, cells)
    
    print(walls)
    print(cells)
    

def gen(x, y, z):
    cells = blank_cells(x, y, z)
    walls = blank_walls(x, y, z, cells)
    check = 1
    
    while len(walls) > 0:
        wall = choice(walls)
        place_wall(wall, cells, check)
        walls.remove(wall)
        check += 1

def blank_maze2(x, y, z):
    cells_3D = []
    walls = []
    
    for xindex in range(x):
        cells_2D = []
        for yindex in range(y):
            cells_1D = []
            for zindex in range(z):
                new_cell = Cell(1 - (xindex == 0), 1 - (yindex == 0), 1 - (zindex == 0))
                cells_1D.append(new_cell)
                if new_cell.west == 1:
                    walls.append((xindex, yindex, zindex, 1))
                if new_cell.south == 1:
                    walls.append((xindex, yindex, zindex, 2))
                if new_cell.down == 1:
                    walls.append((xindex, yindex, zindex, 3))
            cells_2D.append(cells_1D)
        cells_3D.append(cells_2D)
    
    return cells_3D, walls

def blank_cells(x, y, z):
    
    cells_3D = []
    for xindex in range(x):
        cells_2D = []
        for yindex in range(y):
            cells_1D = []
            for zindex in range(z):
                cells_1D.append(Cell(xindex, yindex, zindex))
            cells_2D.append(cells_1D)
        cells_3D.append(cells_2D)
    
    return cells_3D

def blank_walls(x, y, z, cells):
    
    walls = []
    for xindex in range(x):
        for yindex in range(y):
            for zindex in range(z):
                xwall = Wall(cells[xindex][yindex][zindex], 'w')
                ywall = Wall(cells[xindex][yindex][zindex], 's')
                zwall = Wall(cells[xindex][yindex][zindex], 'd')
                
                if xindex + 1 == x:
                    Wall(cells[xindex][yindex][zindex], 'e', 0)
                if xindex == 0:
                    xwall.set_state(0)
                else:
                    xwall.link_cell(cells[xindex-1][yindex][zindex], 'e')
                    walls.append(xwall)

                if yindex + 1 == y:
                    Wall(cells[xindex][yindex][zindex], 'n', 0)
                if yindex == 0:
                    ywall.set_state(0)
                else:
                    ywall.link_cell(cells[xindex][yindex-1][zindex], 'n')
                    walls.append(ywall)

                if zindex + 1 == z:
                    Wall(cells[xindex][yindex][zindex], 'u', 0)
                if zindex == 0:
                    zwall.set_state(0)
                else:
                    zwall.link_cell(cells[xindex][yindex][zindex-1], 'u')
                    walls.append(zwall)

    return walls

def place_wall(wall, cells, check):
    if wall.state != 1 or len(wall.cells) != 2:
        return False
    wall.set_state(0)
    if not check_path(wall.cells.items()[0], wall.cells.items()[1], cells, check):
        wall.set_state(-1)
        return False
    return True

def check_path(current_cell, target_cell, cells, check):
    current_cell.check = check
    
    for side, wall in current_cell.walls.items():
        if wall.state == 1:
            next_cell = cells[XYZ_nsew(side)[0]+current_cell.x][XYZ_nsew(side)[1]+current_cell.y][XYZ_nsew(side)[2]+current_cell.z]
            if next_cell == target_cell:
                return True
            elif next_cell.check < check:
                check_path(next_cell, target_cell, cells, check)
    return False


def NSEW_xyz(xyz):
    if xyz[0] == 1:
        return 'e'
    elif xyz[0] == -1:
        return 'w'
    if xyz[1] == 1:
        return 'n'
    elif xyz[1] == -1:
        return 's'
    if xyz[2] == 1:
        return 'u'
    elif xyz[2] == -1:
        return 'd'
    
def XYZ_nsew(nsew):
    if nsew == 'e':
        return [1,0,0]
    elif nsew == 'w':
        return [-1,0,0]
    if nsew == 'n':
        return [0,1,0]
    elif nsew == 's':
        return [0,-1,0]
    if nsew == 'u':
        return [0,0,1]
    elif nsew == 'd':
        return [0,0,-1]

if __name__ == '__main__':
    sys.exit(main())
