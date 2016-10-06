
class Cell(object):
    
    def __init__(self, xyz):
        self.bread_crumbs = 0
        self.walls = {}
        self.xyz = xyz

    def add_wall(self, wall, xyz):
        self.walls[xyz] = wall

    def set_state(self, state, xyz):
        if self.walls.__contains__(xyz):
            self.walls[xyz].state = state

    def check_crumbs(self, c):
        return self.bread_crumbs < c
    
    def drop_bread_crumbs(self, crumbs):
        self.bread_crumbs = crumbs

    def __repr__(self):
        sides = ""
        for wall in self.walls.values():
            sides = sides + " " + str(wall.state)
        return "C:%s%s%s" % self.xyz + sides