
from random import choice
import sys

from com.nineteengiraffes.Cell import Cell
from com.nineteengiraffes.Wall import Wall


def main():
    gen(2, 2, 1)


def gen(x, y, z):
    cells = blank_cells(x, y, z)
    walls = blank_walls(x, y, z, cells)
    crumbs = 1
    
    print(walls)
    print(cells)
    
    while len(walls) > 0:
        wall = choice(walls)
        place_wall(wall, cells, crumbs)
        walls.remove(wall)
        crumbs += 1
        
    print(walls)
    print(cells)

def blank_cells(x, y, z):
    
    cells_3D = []
    for xindex in range(x+2):
        cells_2D = []
        for yindex in range(y+2):
            cells_1D = []
            for zindex in range(z+2):
                cells_1D.append(Cell((xindex, yindex, zindex)))
            cells_2D.append(cells_1D)
        cells_3D.append(cells_2D)
    
    return cells_3D

def blank_walls(xmax, ymax, zmax, cells):
    
    walls = []
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            for z in range(1, zmax + 1):
                xwall = Wall(cells[x][y][z], cells[x - 1][y][z])
                ywall = Wall(cells[x][y][z], cells[x][y - 1][z])
                zwall = Wall(cells[x][y][z], cells[x][y][z - 1])
                
                if x == xmax:
                    Wall(cells[x + 1][y][z], cells[x][y][z], 0)
                
                if x == 1:
                    xwall.set_state(0)
                else:
                    walls.append(xwall)
                
                if y == ymax:
                    Wall(cells[x][y + 1][z], cells[x][y][z], 0)
                
                if y == 1:
                    ywall.set_state(0)
                else:
                    walls.append(ywall)
                
                if z == zmax:
                    Wall(cells[x][y][z + 1], cells[x][y][z], 0)
                
                if z == 1:
                    zwall.set_state(0)
                else:
                    walls.append(zwall)
    
    return walls

def place_wall(wall, cells, crumbs):
    if wall.state != 1:
        return False
    wall.set_state(0)
    print(wall)
    if not check_path(wall.cells[0], wall.cells[1], cells, crumbs):
        wall.set_state(-1)
        return False
    return True

def check_path(current_cell, target_cell, cells, crumbs):
    current_cell.drop_bread_crumbs(crumbs)
    print(str(current_cell) + " " + str(target_cell) + " b" + str(crumbs))
    for xyz, wall in current_cell.walls.items():
        if wall.state == 1:
            next_cell = cells[xyz[0]][xyz[1]][xyz[2]]
            if next_cell == target_cell:
                return True
            elif next_cell.check_crumbs(crumbs):
                check_path(next_cell, target_cell, cells, crumbs)
    return False


if __name__ == '__main__':
    sys.exit(main())
