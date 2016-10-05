
class Cell(object):
    
    def __init__(self, x, y, z):
        self.check = 0
        self.walls = {}
        self.x = x
        self.y = y
        self.z = z

    def add_wall(self, wall, side):
        self.walls[side] = wall

    def set_state(self, state, side):
        if self.walls.__contains__(side):
            self.walls[side].state = state

    def __repr__(self):
        sides = ""
        for key, wall in self.walls.items():
            sides = sides + " " + key + str(wall.state)
        return "C: %s%s%s S:" % (self.x,self.y,self.z) + sides