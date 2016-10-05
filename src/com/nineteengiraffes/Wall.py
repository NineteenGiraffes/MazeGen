
class Wall(object):

    'state: Wall=0 Hallway=-1 Unset=1'

    def __init__(self, cell, side, state=1):
        self.cells = {}
        self.state = state
        self.cells[side] = cell
        cell.add_wall(self, side)

    def link_cell(self, cell, side):
        self.cells[side] = cell
        cell.add_wall(self, side)

    def set_state(self, state):
        self.state = state
        
    def __repr__(self):
        sides = ""
        for key in self.cells.keys():
            sides = sides + key
        return "S: " + sides + str(self.state)