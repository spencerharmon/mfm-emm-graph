from mfm_griddata_parser.grid_data import GridData
from .atoms import Identifier
from .cell import Cell
from pprint import pprint

class Grid(GridData):
    def __init__(self, mfm_grid_state_json_file):
        super().__init__(mfm_grid_state_json_file)
        self.cells = [Cell(self, _id, idx, idy) for _id, idx, idy in self.find_identifiers()]

    def get_atom_types(self):
        ret = super().get_atom_types() #nonetype if the update is done here. wat?
        ret.update({'Identifier': Identifier})
        return ret

    def find_identifiers(self):
        return [(Identifier(atom), atom["x"], atom["y"])
                for atom in self.event_layer_atom_data
                if atom["name"] == "Identifier"]
