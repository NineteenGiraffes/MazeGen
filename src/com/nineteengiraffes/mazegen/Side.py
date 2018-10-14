
class Side(object):
    
    def __init__(self, cell1, cell2, state=-1):
        self.cells = [cell1, cell2]         # list of adjacent Cells
        self.state = state                  # state: Wall=1 Hallway=0 Unset=-1
        cell1._add_side(self, cell2.xyz)    # adds this sides to adjacent Cells
        cell2._add_side(self, cell1.xyz)

    def set_state(self, state): # set the state of this side
        self.state = state
        
    def __repr__(self):
        return "W:%s,%s,%s/" % self.cells[0].xyz + "%s,%s,%s " % self.cells[1].xyz + str(self.state)
