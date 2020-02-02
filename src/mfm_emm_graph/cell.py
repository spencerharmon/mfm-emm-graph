from .atoms import Identifier, Empty
from .exceptions import MembraneNotFound
from pprint import pprint
from graph_tools import *

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

        self.graph = Graph()
        self.vprop_genes = self.graph.new_vertex_property("object")
        for atom in self.atoms_in_cell:
            if "treeid" in atom.data_members.keys():
                self.vprop_genes[int(self.graph.add_vertex())] = atom
        
        

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
                self.flood_fill(d_x, d_y)

        
    def print_cell_grid(self):
        for list in self.cell_grid:
            print(*list, sep='')



