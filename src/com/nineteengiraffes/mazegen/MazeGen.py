
from collections import deque
from math import sqrt
from random import choice, sample

from com.nineteengiraffes.mazegen.Cell import Cell
from com.nineteengiraffes.mazegen.Side import Side


class MazeGen():

    cells = None    # to be 3D array of Cell objects
    sides = None    # to be set of interior Side objects
    steps = 0       # counter
    trips = []      # log/counter


# blank maze setup
    def gen_empty(self, x, y, z):   # initialize Cells and Sides
        
        self.cells = self._gen_empty_cells(x, y, z) # initialize Cell 3D array
        self.sides = self._gen_empty_sides(x, y, z) # initialize interior Side set

    def _gen_empty_cells(self, x, y, z):    # returns a 3D array of new Cell objects
        
        cells_3D = []
        for xindex in range(x+2):   # includes 'ghost' Cells on the outside of the exterior sides
            cells_2D = []
            for yindex in range(y+2):
                cells_1D = []
                for zindex in range(z+2):
                    cells_1D.append(Cell((xindex, yindex, zindex))) # Cell identifier is a tuple (x,y,z)
                cells_2D.append(cells_1D)
            cells_3D.append(cells_2D)
        
        return cells_3D

    def _gen_empty_sides(self, xmax, ymax, zmax):   # returns a list of new interior Side objects
        
        new_sides = list()
        for x in range(1, xmax + 1):    # start at 1 because 'ghost' Cells don't get sides
            for y in range(1, ymax + 1):
                for z in range(1, zmax + 1):
                    xwall = Side(self.cells[x][y][z], self.cells[x - 1][y][z])  # new Side on the negative x side of Cell
                    ywall = Side(self.cells[x][y][z], self.cells[x][y - 1][z])  # new Side on the negative y side of Cell
                    zwall = Side(self.cells[x][y][z], self.cells[x][y][z - 1])  # new Side on the negative z side of Cell
                    
                    if x == xmax:                                               # also create a new exterior Side on the positive x side of Cell for last Cell
                        Side(self.cells[x + 1][y][z], self.cells[x][y][z], 1)
                    
                    if x == 1:              # make the first Side exterior
                        xwall.set_state(1)  
                    else:
                        new_sides.append(xwall) # if not exterior, add to interior side set
                    
                    if y == ymax:                                               # also add a new exterior Side on the positive y side of Cell for last Cell
                        Side(self.cells[x][y + 1][z], self.cells[x][y][z], 1)
                    
                    if y == 1:              # make the first Side exterior
                        ywall.set_state(1)
                    else:
                        new_sides.append(ywall) # if not exterior, add to interior side set
                    
                    if z == zmax:                                               # also add a new exterior Side on the positive z side of Cell for last Cell
                        Side(self.cells[x][y][z + 1], self.cells[x][y][z], 1)
                    
                    if z == 1:              # make the first Side exterior
                        zwall.set_state(1)
                    else:
                        new_sides.append(zwall) # if not exterior, add to interior side set
        
        return new_sides
         

# Maze generation


    def random_side_fill(self, depth_first=True, log=False):	# set state of all sides randomly to create maze using depth first or breadth first search 
        path_marker = 1              # marker for path checks
        
        while len(self.sides) > 0:      # continue till all sides are set
            side = choice(self.sides)   # pick random side
        
            if side.state == -1:        # verify side state is unset
                side.set_state(1)       # set state to 'wall'
                self.steps = 0
                if depth_first:
                    if not self.check_path_d(side.cells[0], side.cells[1], path_marker, log):   # if path check fails, set state to 'hallway'
                        side.set_state(0)
                else:
                    if not self.check_path_b(side.cells[0], side.cells[1], path_marker, log):   # if path check fails, set state to 'hallway'
                        side.set_state(0)
                    
            self.sides.remove(side)     # remove Side from set
            path_marker += 1
            self.trips.append(self.steps)
        avg_trip = sum(self.trips) / len(self.trips)
        if log:
            print("Trips: " + str(len(self.trips)) + " Avg: " + str(round(avg_trip)) + " " + str(round(avg_trip/len(self.trips),3)) + " Cells: " + str((len(self.cells)-2) * (len(self.cells[0])-2) * (len(self.cells[0][0])-2)))
            print(str(self.trips))              # dead end trips take many steps
        self.clear_path_markers()         # clear all path markers

    def random_cell_explore_out(self, pop=False, log=False):	# start at a random cell and build out with sample() or pop()
        x = choice(range(1, len(self.cells) - 1))
        y = choice(range(1, len(self.cells[x]) - 1))
        z = choice(range(1, len(self.cells[x][y]) - 1))
        starting_cell = self.cells[x][y][z]             # pick random cell
        
        explored_cells = set()                          # explored cells
        unexplored_sides = starting_cell.unset_sides()   # unexplored sides of start cell
        explored_cells.add(starting_cell)
        self.steps = 0
        if log:
            print("- %s C:%s S:%s" % (self.steps, len(explored_cells),len(unexplored_sides)))
        
        while len(unexplored_sides) > 0:      # continue till all side are explored
            self.steps += 1
            if pop:
                side = unexplored_sides.pop()
            else:
                side = sample(unexplored_sides,1)[0]
            unexplored_sides.discard(side)

            new_cell = None
            for cell in side.cells:
                if cell not in explored_cells:
                    new_cell = cell
                            
            if new_cell == None:    # already been to both cells so set state to Wall
                side.set_state(1)
                if log:
                    print("1 %s C:%s S:%s" % (self.steps, len(explored_cells),len(unexplored_sides)))
            else:                   # newly explored cell so set state to Hallway
                side.set_state(0)
                unexplored_sides.update(new_cell.unset_sides())  # add unexplored sides for newly explored cell
                explored_cells.add(new_cell)
                if log:
                    print("0 %s C:%s S:%s" % (self.steps, len(explored_cells),len(unexplored_sides)))

        return

    def check_path_b(self, start_cell, target_cell, path_marker, log):    	# returns true if path exists from start_cell to target_cell (uses breath first)
        current_cell = start_cell                           # remember start cell for back tracking
        cell_stack = deque()                                # empty stack
        current_cell.mark_as_visited(path_marker)           # mark start cell as visited
        
        while True:
            current_cell.reset_viable_sides_id()
            for xyz in current_cell.viable_sides_id:
                next_cell = self.cells[xyz[0]][xyz[1]][xyz[2]]
                if next_cell.is_unvisited(path_marker):                 # if unvisited, add to stack
                    if next_cell == target_cell:                        # return if target cell reached
                        if log:
                            print(str(next_cell) + " " + str(target_cell) + " T  Step " + str(self.steps) + " " + str(len(cell_stack)))
                        return True
                    next_cell.mark_as_visited(path_marker)
                    cell_stack.append(next_cell)
                    self.steps += 1
            if cell_stack:
                current_cell = cell_stack.popleft()
                
            else:
                if log:
                    print(str(current_cell) + " " + str(target_cell) + "  F Step " + str(self.steps))
                return False

    def check_path_d(self, start_cell, target_cell, path_marker, log):  	    # returns true if path exists from start_cell to target_cell (uses depth first)
        current_cell = start_cell                           # remember start cell for back tracking
        current_cell.mark_as_visited(path_marker)           # mark start cell as visited
        current_cell.reset_viable_sides_id()                # reset cell sides
        
        while True:
            if len(current_cell.viable_sides_id) > 0:                 # if there are unchecked sides, pick one
                
                current_cell.viable_sides_id.sort(key=self.xyz_sort(target_cell.xyz), reverse=True) # orders list so last side is closest to the target cell
                xyz = current_cell.viable_sides_id.pop()
                next_cell = self.cells[xyz[0]][xyz[1]][xyz[2]]
                if next_cell == target_cell:                        # return if target cell reached
                    if log:
                        print(str(current_cell) + " " + str(target_cell) + " T  Step " + str(self.steps))
                    return True
                if next_cell.is_unvisited(path_marker):               # if picked side is unvisited, jump to next cell 
                    next_cell.back_track_cell = current_cell
                    next_cell.mark_as_visited(path_marker)
                    next_cell.reset_viable_sides_id()
                    current_cell = next_cell
                    self.steps += 1
                continue
            elif current_cell == start_cell:       # this is the starting cell and no more back tracking is possible
                if log:
                    print(str(current_cell) + " " + str(target_cell) + "  F Step " + str(self.steps))
                return False
            else:
                current_cell = current_cell.back_track_cell         # back track one step

    def check_path_r(self, start_cell, target_cell, path_marker):    	# returns true if path exists from start_cell to target_cell (uses recursion, only tiny mazes clear the python recursion limit)
        
        start_cell.mark_as_visited(path_marker)                  # mark cell as visited
        for xyz, side in start_cell.sides.items():
            if side.state != 1:                                 # skip to next side if side is a 'wall'
                next_cell = self.cells[xyz[0]][xyz[1]][xyz[2]]
                if next_cell == target_cell:                    # return if target cell reached
                    return True
                elif next_cell.is_unvisited(path_marker):            # continue if unvisited
                    if self.check_path_r(next_cell, target_cell, path_marker): # check path from the next cell
                        return True
        return False

    def clear_path_markers(self):	# reset path_marker for all Cells to unvisited
        
        for cells_2D in self.cells:
            for cells_1D in cells_2D:
                for cell in cells_1D:
                    cell.mark_as_visited(0)

    def xyz_sort(self, xyz2):       # returns function: key_xyz for use in sorting by distance
        def key_xyz(xyz1):          # returns the distance from xyz1 to xyz2
            dist = sqrt((xyz1[0]-xyz2[0])**2 + (xyz1[1]-xyz2[1])**2 + (xyz1[2]-xyz2[2])**2)   # distance formula xyz1 to xyz2
            return dist
        return key_xyz

# outputs


    def convert_to_bit_array(self): # returns a 3D array of 6bit numbers representing each cell
        
        d3 = []
        for cells_2D in self.cells:
            d2 = []
            for cells_1D in cells_2D:
                d1 = []
                for cell in cells_1D:
                    bit = 000000    # 6 bits to represent the 6 sides of each cell
                    for xyz, wall in cell.sides.items():            # xyz is the Cell on the opposite side of wall 
                        if wall.state != -1:                        # ignore unset Walls
                            if xyz[0] != cell.xyz[0]:               # is the wall is on the x axis
                                if xyz[0] < cell.xyz[0]:            
                                    bit = bit | (wall.state << 0)   # if the wall is on the negative x side, set the 1st bit to the wall state
                                else:
                                    bit = bit | (wall.state << 3)   # if the wall is on the positive x side, set the 4th bit to the wall state
                                    
                            elif xyz[1] != cell.xyz[1]:             # is the wall is on the y axis
                                if xyz[1] < cell.xyz[1]:
                                    bit = bit | (wall.state << 1)   # if the wall is on the negative y side, set the 2nd bit to the wall state
                                else:
                                    bit = bit | (wall.state << 4)   # if the wall is on the positive y side, set the 5th bit to the wall state
                                    
                            elif xyz[2] != cell.xyz[2]:             # is the wall is on the z axis
                                if xyz[2] < cell.xyz[2]:
                                    bit = bit | (wall.state << 2)   # if the wall is on the negative z side, set the 3nd bit to the wall state
                                else:
                                    bit = bit | (wall.state << 5)   # if the wall is on the positive z side, set the 6th bit to the wall state
                    d1.append(bit)
                d2.append(d1)
            d3.append(d2)
        return d3
 
    def print_ascii(self):  # print ascii representation of cells and sides (the maze)

        for x in range(1, len(self.cells) - 1):
            print(" ")                              # spacer between levels
            print("level " + str(x))
            for y in range(1, len(self.cells[x]) - 1):
                print_string_0 = ""
                print_string_1 = ""
                print_string_2 = ""
                for z in range(1, len(self.cells[x][y]) - 1):# ↓↑↕
                    x_output = " ↕ "                # set x to up and down 'hallway'
                    x_up_down = 0                   # no wall up or down
                    y_output = "   "                # set y to 'hallway'
                    z_output = " "                  # set z to 'hallway'
                    for xyz, wall in self.cells[x][y][z].sides.items():
                        if xyz[0] < x and wall.state == 1:      # there is a wall up
                            x_up_down += 1
                        elif xyz[0] > x and wall.state == 1:    # there is a wall down
                            x_up_down += 10
                        elif xyz[1] < y and wall.state == 1:    # set y to 'wall'
                            y_output = "---"
                        elif xyz[2] < z and wall.state == 1:    # set z to 'wall'
                            z_output = "|"
                            
                        if x_up_down == 1:                      # set x to 'wall above'
                            x_output = " ↓ "
                        elif x_up_down == 10:                   # set x to 'wall below'
                            x_output = " ↑ "
                        elif x_up_down == 11:                   # set x to 'wall above and below'
                            x_output = "   "
                            
                    print_string_0 += "+" + y_output            # build string for top of cells
                    print_string_1 += z_output + x_output       # build string for center of cells
                    print_string_2 += "+---"                    # build string for bottom of cells
                print(print_string_0 + "+")                 # print top of cells in this row
                print(print_string_1 + "|")                 # print center of cells in this row
            print(print_string_2 + "+")                 # print bottom of cells only on last row of each level


    def run(self): # runs the generator
        while True:
            try:
                x = int(input("Maze depth: (1 - 15) "))
                break
            except:
                print("    Please input an integer in range")
        
        while True:
            try:
                y = int(input("Maze height: (1 - 15) "))
                break
            except:
                print("    Please input an integer in range")
        while True:
            try:
                z = int(input("Maze width: (1 - 40) "))
                break
            except:
                print("    Please input an integer in range")
                
        self.gen_empty(x, y, z)
        print(" ")
        
        while True:
            gen_type = input("Explore or Spot fill: (E/S) ")
            if gen_type == "E" or gen_type == "e":
                pop = False
                while True:
                    gen_type = input("Random or Ordered: (R/O) ")
                    if gen_type == "R" or gen_type == "r":
                        break
                    elif gen_type == "O" or gen_type == "o":
                        pop = True
                        break
                    else:
                        print("    Please choose 'r' or 'o'")
                
                log = (input("Generate Maze! (return)") == "log")
                if (not log) and (x*y*z > 9000):
                    print("please wait...")
                self.random_cell_explore_out(pop, log)
                break
            elif gen_type == "S" or gen_type == "s":
                depth_first = False
                while True:
                    gen_type = input("Depth first or Breadth first: (B/D) ")
                    if gen_type == "B" or gen_type == "b":
                        break
                    elif gen_type == "D" or gen_type == "d":
                        depth_first = True
                        break
                    else:
                        print("    Please choose 'b' or 'd'")
                log = (input("Generate Maze! (return)") == "log")
                if (not log) and (x*y*z > 600):
                    print("please wait...")
                self.random_side_fill(depth_first, log)
                break
            else:
                print("    Please choose 'e' or 's'")
            
#        simple_3d_array_for_export = self.convert_to_bit_array()
        self.print_ascii()
        

MazeGen().run()
