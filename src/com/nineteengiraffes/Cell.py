
class Cell(object):
    
    def __init__(self, xyz):
        self._bread_crumbs = 0
        self.walls = {}
        self.xyz = xyz

    def _add_wall(self, wall, xyz):
        self.walls[xyz] = wall

    def check_crumbs(self, c):
        return self._bread_crumbs < c
    
    def drop_bread_crumbs(self, crumbs):
        self._bread_crumbs = crumbs

    def __repr__(self):
        sides = ""
        for wall in self.walls.values():
            sides = sides + " " + str(wall.state)
        return "C:%s%s%s" % self.xyz + sides