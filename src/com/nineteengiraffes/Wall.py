
class Wall(object):

    'state: Wall=0 Hallway=-1 Unset=1'

    def __init__(self, cell1, cell2, state=1):
        self.cells = [cell1, cell2]
        self.state = state
        cell1.add_wall(self, cell2.xyz)
        cell2.add_wall(self, cell1.xyz)


    def set_state(self, state):
        self.state = state
        
    def __repr__(self):
        return "W:%s%s%s/" % self.cells[0].xyz + "%s%s%s " % self.cells[1].xyz + str(self.state)