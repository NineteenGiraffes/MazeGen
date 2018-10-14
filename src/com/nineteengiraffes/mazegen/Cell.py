
class Cell(object):
    
    def __init__(self, xyz):
        self._path_marker = 0  # marker for path finding
        self.viable_sides_id = list() # list of IDs of sides viable for navigation (non solid)
        self.back_track_cell = None
        self.sides = {}         # dictionary of sides and adjacent cell IDs
        self.xyz = xyz          # cell ID (tuple)

    def _add_side(self, side, xyz): # add side to cell
        self.sides[xyz] = side

    def reset_viable_sides_id(self): # resets viable_sides_id to include all non solid sides
        self.viable_sides_id = list()
        for cell_id, side in self.sides.items():
            if side.state != 1:
                self.viable_sides_id.append(cell_id)

    def unset_sides(self): # returns all unset sides
        unset_sides = set()
        for side in self.sides.values():
            if side.state == -1:
                unset_sides.add(side)
        return unset_sides

    def is_unvisited(self, path_marker): # returns true if cell is unvisited
        return self._path_marker < path_marker

    def mark_as_visited(self, path_marker): # marks the cell with the current crumb
        self._path_marker = path_marker

    def __repr__(self):
        return "C:%s,%s,%s" % self.xyz
