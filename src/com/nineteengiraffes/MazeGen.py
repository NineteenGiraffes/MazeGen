
from random import choice

from GUI import Application, Button, Label, View, Window

from com.nineteengiraffes.Cell import Cell
from com.nineteengiraffes.Wall import Wall


class MazeGen(Application):

    cells = None
    walls = None
#     steps = 0
    
    def gen_empty(self, x, y, z):
        
        self.cells = self._gen_empty_cells(x, y, z)
        self.walls = self._gen_empty_walls(x, y, z, self.cells)
        
#         print(self.walls)
#         print(self.cells)
    
    def _gen_empty_cells(self, x, y, z):
        
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

    def _gen_empty_walls(self, xmax, ymax, zmax, cells):
        
        walls = []
        for x in range(1, xmax + 1):
            for y in range(1, ymax + 1):
                for z in range(1, zmax + 1):
                    xwall = Wall(cells[x][y][z], cells[x - 1][y][z])
                    ywall = Wall(cells[x][y][z], cells[x][y - 1][z])
                    zwall = Wall(cells[x][y][z], cells[x][y][z - 1])
                    
                    if x == xmax:
                        Wall(cells[x + 1][y][z], cells[x][y][z], 1)
                    
                    if x == 1:
                        xwall.set_state(1)
                    else:
                        walls.append(xwall)
                    
                    if y == ymax:
                        Wall(cells[x][y + 1][z], cells[x][y][z], 1)
                    
                    if y == 1:
                        ywall.set_state(1)
                    else:
                        walls.append(ywall)
                    
                    if z == zmax:
                        Wall(cells[x][y][z + 1], cells[x][y][z], 1)
                    
                    if z == 1:
                        zwall.set_state(1)
                    else:
                        walls.append(zwall)
        
        return walls
    
    def random_wall_fill(self):
        crumbs = 1
        
        while len(self.walls) > 0:
            wall = choice(self.walls)
        
            if wall.state == -1:
                wall.set_state(1)
#                 print(wall)
#                 self.steps = 0
                if not self.check_path(wall.cells[0], wall.cells[1], crumbs):
                    wall.set_state(0)
#                 print(str(wall.state) + " in " + str(self.steps) + " Steps")
    
            self.walls.remove(wall)
            crumbs += 1
        
        self.clear_all_crumbs()
#         print(self.walls)
#         print(self.cells)
    
    def check_path(self, current_cell, target_cell, crumbs):
        
        current_cell.drop_bread_crumbs(crumbs)
#         self.steps += 1
        
#         print(str(current_cell) + " " + str(target_cell) + " bc" + str(crumbs) + " Step " + str(self.steps))
        for xyz, wall in current_cell.walls.items():
            if wall.state != 1:
                next_cell = self.cells[xyz[0]][xyz[1]][xyz[2]]
                if next_cell == target_cell:
                    return True
                elif next_cell.check_crumbs(crumbs):
                    if self.check_path(next_cell, target_cell, crumbs):
                        return True
        return False
    
    def clear_all_crumbs(self):
        
        for cells_2D in self.cells:
            for cells_1D in cells_2D:
                for cell in cells_1D:
                    cell.drop_bread_crumbs(0)
        
    def convert_to_bit_array(self):
        
        d3 = []
#         print("x")
        for cells_2D in self.cells:
            d2 = []
#             print("y")
            for cells_1D in cells_2D:
                d1 = []
#                 print("z")
                for cell in cells_1D:
                    bit = 0
                    for xyz, wall in cell.walls.items():
                        if wall.state != -1:
                            if xyz[0] != cell.xyz[0]:
                                if xyz[0] < cell.xyz[0]:
                                    bit = bit | (wall.state << 0)
                                else:
                                    bit = bit | (wall.state << 3)
                            elif xyz[1] != cell.xyz[1]:
                                if xyz[1] < cell.xyz[1]:
                                    bit = bit | (wall.state << 1)
                                else:
                                    bit = bit | (wall.state << 4)
                            elif xyz[2] != cell.xyz[2]:
                                if xyz[2] < cell.xyz[2]:
                                    bit = bit | (wall.state << 2)
                                else:
                                    bit = bit | (wall.state << 5)
#                     print(bin(bit))
                    d1.append(bit)
                d2.append(d1)
            d3.append(d2)
        return d3
 
    def print_ascii(self):

        for x in range(1, len(self.cells) - 1):
            print(" ")
            print(" ")
            print_string_2 = ""
            for y in range(1, len(self.cells[x]) - 1):
                print_string_0 = ""
                print_string_1 = ""
                print_string_2 = ""
                for z in range(1, len(self.cells[x][y]) - 1):
                    x_output = "O"
                    y_output = " "
                    z_output = " "
                    for xyz, wall in self.cells[x][y][z].walls.items():
                        if xyz[0] < x and wall.state == 1:
                            x_output = " "
                        elif xyz[1] < y and wall.state == 1:
                            y_output = "-"
                        elif xyz[2] < z and wall.state == 1:
                            z_output = "|"
                    print_string_0 += "+" + y_output
                    print_string_1 += z_output + x_output
                    print_string_2 += "+-"
                print(print_string_0 + "+")
                print(print_string_1 + "|")
            print(print_string_2 + "+")

    def open_app(self):    
        self.gen_empty(x=3, y=3, z=3)
        self.random_wall_fill()
#         self.convert_to_bit_array()
        self.print_ascii()
        
        main_window = Window(style = 'standard', size = (400, 400),)
        main_view = View()
        quit_btn = Button("Quit", action = "quit_cmd", enabled = True)
        main_view.place(quit_btn, left = 50, top = 50)
        main_view.place(Label("Test"), left = 20, top = 20)
        main_window.place(main_view, left = 0, top = 0, right = 0, bottom = 0, sticky = 'nw')
#         main_window.show()
        

# if __name__ == '__main__':
#     pass

MazeGen().run()
    