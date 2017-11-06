
class Cell(object):
    
    def __init__(self, xyz):
        self._bread_crumbs = 0  # marker for path finding r
        self.remaing_sides = {} # dictionary of sides and adjacent cell IDs for path finding d
        self.back_track_cell = None
        self.sides = {}         # dictionary of sides and adjacent cell IDs
        self.xyz = xyz          # cell ID (tuple)

    def _add_side(self, side, xyz): # add side to dictionary
        self.sides[xyz] = side

    def check_crumbs(self, crumbs):  # returns true if cell does not have the current crumb count
        return self._bread_crumbs < crumbs
    
    def drop_bread_crumbs(self, crumbs):    # marks the cell with the current crumb count
        self._bread_crumbs = crumbs

    def __repr__(self):
        walls = ""
        for side in self.sides.values():
            walls = walls + " " + str(side.state)
#         walls = walls + ", "
#         for side in self.remaing_sides.values():
#             walls = walls + " " + str(side.state)
        return "C:%s%s%s" % self.xyz + walls