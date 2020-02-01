from mfm_griddata_parser.grid_data import GridData
from .atoms import Atom, Empty, Identifier
from .cell import Cell
from pprint import pprint

class Grid(object):
    """
    represents the MFM grid. 
    """
    def __init__(self, mfm_grid_state_file):
        self.grid_data = GridData()
        self.grid_data.load_file(mfm_grid_state_file)
        self.atom_data = self.grid_data.get_grid_state()["non_empty_site_list"]
        self.atom_index = self.index_atoms()
        self.cells = [Cell(self, _id, idx, idy) for _id, idx, idy in self.find_identifiers()]

    def find_identifiers(self):
        return [(Identifier(atom), atom["x"], atom["y"])
                for atom in self.atom_data
                if atom["name"] == "Identifier"]

    def gen_2d_grid_list(self, init):
        """
        generates a 2d list matching the size of our grid with valies initialized
        to the object given by init
        """
        return [[init
                 for x in range(0, self.grid_data.grid_height)]
                for y in range(0, self.grid_data.grid_width)]

    def index_atoms(self):
        """
        index atoms in 2d list
        """
        
        two_d_list = self.gen_2d_grid_list(self.atom_factory({"name": "Empty"}))
        i = 0
        for a in two_d_list[0]:
            i += 1
        print("row width: " + i.__str__())
        c = 0
        for a in two_d_list:
            c += 1
        print("num rows: " + c.__str__())
        for a_d in self.atom_data:
            two_d_list[a_d["x"]][a_d["y"]] = self.atom_factory(a_d)
        return two_d_list

    def atom_factory(self, atom_dict):
        """
        return a special atom class type (should be used only for type hinting) or a generic atom
        """
        return (Identifier if atom_dict["name"] == "Identifier" else
                Empty if atom_dict["name"] == "Empty" else
                Atom)(atom_dict)

    def get_atom_in_site(self, x, y):
        return self.atom_index[x][y]

    def print_grid_ascii(self):
        for list in self.atom_index:
            print(*list, sep='')
