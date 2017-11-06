
from random import choice

from GUI import Application#, Button, Label, View, Window

from com.nineteengiraffes.Cell import Cell
from com.nineteengiraffes.Side import Side


class MazeGen(Application):

    cells = None    # to be 3D array of Cell objects
    sides = None    # to be set of interior Side objects
    steps = 0
    trips = []


# blank maze setup
    def gen_empty(self, x, y, z):   # initialize Cells and Sides
        
        self.cells = self._gen_empty_cells(x, y, z) # initialize Cell 3D array
        self.sides = self._gen_empty_sides(x, y, z) # initialize interior Side set
        
#         print(self.sides)
#         print(self.cells)

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

    def _gen_empty_sides(self, xmax, ymax, zmax):   # returns a set of new interior Side objects
        
        new_sides = []
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
    def random_side_fill(self): # set state of all sides randomly to create maze
        crumbs = 1              # marker for path checks
        
        while len(self.sides) > 0:      # continue till all sides are set
            side = choice(self.sides)   # pick random side
        
            if side.state == -1:        # verify side state is unset
                side.set_state(1)       # set state to 'wall'
#                 print(side)
                self.steps = 0
                if not self.check_path_d(side.cells[0], side.cells[1]):   # if path check fails, set state to 'hallway'
#                 if not self.check_path_r(side.cells[0], side.cells[1], crumbs):   # if path check fails, set state to 'hallway'
                    side.set_state(0)
#                 print(str(side.state) + " in " + str(self.steps) + " Steps")
    
            self.sides.remove(side)     # remove Side from set
            crumbs += 1
            self.trips.append(self.steps)
        avg_trip = sum(self.trips) / len(self.trips)
        
        print("Trips: " + str(len(self.trips)) + " Avg: " + str(round(avg_trip)) + " " + str(round(avg_trip/len(self.trips),2)) + " Cells: " + str((len(self.cells)-2) * (len(self.cells[0])-2) * (len(self.cells[0][0])-2)))
        
        self.clear_all_crumbs()         # clear all path markers
#         print(self.sides)
#         print(self.cells)

    def check_path_d(self, current_cell, target_cell):      # returns true if path exists from current_cell to target_cell (uses depth first)
        self.open_path()
        current_cell.back_track_cell = target_cell            # mark this cell as the start, can't back track past here
        
        while True:
            self.steps += 1
            if len(current_cell.remaing_sides) > 0:                 # if there are unchecked sides, pick one
                
                xyz = current_cell.remaing_sides.popitem()[0]
                next_cell = self.cells[xyz[0]][xyz[1]][xyz[2]]
                next_cell.remaing_sides.pop(current_cell.xyz, None)
                if next_cell == target_cell:                        # return if target cell reached
#                     print(str(current_cell) + " " + str(target_cell) + " T Step " + str(self.steps))
                    return True
                if next_cell.back_track_cell is None:               # if picked side is unvisited, jump to next cell 
                    next_cell.back_track_cell = current_cell
                    current_cell = next_cell
                continue
            elif current_cell.back_track_cell is target_cell:       # this is the starting cell and no more back tracking is possible
#                 print(str(current_cell) + " " + str(target_cell) + " F Step " + str(self.steps))
                return False
            else:
                current_cell = current_cell.back_track_cell         # back track one step

    def check_path_r(self, current_cell, target_cell, crumbs):    # returns true if path exists from current_cell to target_cell (uses recursion)
        
        current_cell.drop_bread_crumbs(crumbs)                  # mark cell as visited
#         self.steps += 1
        
#         print(str(current_cell) + " " + str(target_cell) + " bc" + str(crumbs) + " Step " + str(self.steps))
        for xyz, side in current_cell.sides.items():
            if side.state != 1:                                 # skip to next side if side is a 'wall'
                next_cell = self.cells[xyz[0]][xyz[1]][xyz[2]]
                if next_cell == target_cell:                    # return if target cell reached
                    return True
                elif next_cell.check_crumbs(crumbs):            # continue if unvisited
                    if self.check_path_r(next_cell, target_cell, crumbs): # check path from the next cell
                        return True
        return False

    def open_path(self): # reset remaining_sides in all cells to include all open sides (unset or 'hallway')
        
        for cells_2D in self.cells:
            for cells_1D in cells_2D:
                for cell in cells_1D:
                    cell.remaing_sides = {}
                    cell.back_track_cell = None
                    for cell_id, side in cell.sides.items():
                        if side.state != 1:
                            cell.remaing_sides[cell_id] = side

    def clear_all_crumbs(self): # reset bread crumbs for all Cells to 0
        
        for cells_2D in self.cells:
            for cells_1D in cells_2D:
                for cell in cells_1D:
                    cell.drop_bread_crumbs(0)


# outputs
    def convert_to_bit_array(self): # returns a 3D array of 6bit numbers representing each cell
        
        d3 = []
#         print("x")
        for cells_2D in self.cells:
            d2 = []
#             print("y")
            for cells_1D in cells_2D:
                d1 = []
#                 print("z")
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
#                     print(bin(bit))
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


# run app
    def open_app(self): # runs the generator
        self.gen_empty(x=2, y=3, z=22)
        self.random_side_fill()
#         self.convert_to_bit_array()
        self.print_ascii()
#         self.cells[1][1][1].remaing_sides = {}
#         print(str(self.cells[1][1][1]))
#         for id, side in self.cells[1][1][1].sides.items():         
#             self.cells[1][1][1].remaing_sides[id] = side
#          
#         print(str(self.cells[1][1][1]))
#         new_side = self.cells[1][1][1].remaing_sides.pop((1,1,2))
#         self.open_path()
#         print(str(self.cells[1][2][1]))
        
        
#         main_window = Window(style = 'standard', size = (400, 400),)
#         main_view = View()
#         quit_btn = Button("Quit", action = "quit_cmd", enabled = True)
#         main_view.place(quit_btn, left = 50, top = 50)
#         main_view.place(Label("Test"), left = 20, top = 20)
#         main_window.place(main_view, left = 0, top = 0, right = 0, bottom = 0, sticky = 'nw')
#         main_window.show()
        

# if __name__ == '__main__':
#     pass

MazeGen().open_app()
    