from .atoms import Identifier, Empty
from .exceptions import MembraneNotFound
from pprint import pprint

class Cell(object):
    def __init__(self, grid, identifier: Identifier, idx, idy):
        self.grid = grid
        self.identifier = identifier
        self.idx = idx
        self.idy = idy
        self.atoms_in_cell = []
        self.cell_grid = self.grid.gen_2d_grid_list(Empty())
        self.is_cell_slot_grid = self.grid.gen_2d_grid_list(False)
        self.flood_fill(self.idx, self.idy)
        self.allowed_x_steps = self.grid.grid_data.grid_width
        self.allowed_y_steps = self.grid.grid_data.grid_height

    def flood_fill(self, x, y):
        """
        Good ol fashioned flood fill. Hopefully recursion depth doesn't get out of hand.
        OuterMembranes are the boundary. Identifier is the starting point.
        Haven't really solved the broken border problem yet. That's ok for now.
        """
        #first check if we already found this one:
        if self.is_cell_slot_grid[x][y]:
            return
        atom = self.grid.atom_index[x][y]

        # if it's an OuterMembrane, it's not in the cell, otherwise it is.
        if atom.name == "OuterMembrane":
            return
        else:
            self.cell_grid[x][y] = atom
            self.is_cell_slot_grid[x][y] = True
            self.atoms_in_cell.append(atom)

            #8-way tail recursion
            for d_x, d_y in [(x + lx, y + ly) for lx in range(-1, 2) for ly in range(-1, 2)]:
                print('recurse ' + str(d_x) + ',' + str(d_y))
                self.flood_fill(d_x, d_y)


        
    def print_cell_grid(self):
        for list in self.cell_grid:
            print(*list, sep='')



