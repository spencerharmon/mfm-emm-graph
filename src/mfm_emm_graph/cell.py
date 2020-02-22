from .atoms import Identifier, Empty
from .exceptions import MembraneNotFound
from pprint import pprint
from graph_tool.all import *
from io import FileIO, StringIO,BytesIO, TextIOWrapper
from tempfile import NamedTemporaryFile
from graph_tool.draw import graph_draw
import html

class Cell(object):
    def __init__(self, grid, identifier: Identifier, idx, idy):
        self.grid = grid
        self.identifier = identifier
        self.id = self.identifier.data_members["id"]
        self.idx = idx
        self.idy = idy
        self.atoms_in_cell = []
        self.cell_grid = self.grid.gen_2d_grid_list(Empty())
        self.is_cell_slot_grid = self.grid.gen_2d_grid_list(False)
        self.flood_fill(self.idx, self.idy)

        self.tree_graphs = self.gen_tree_graphs()

        
    def gen_tree_graphs(self):
        root_genes = [atom for atom in self.atoms_in_cell
                      if atom.name in {"Root",
                                       "ComOut",
                                       "Direction",
                                       "Movement"}]
        graphs = []

        for root in root_genes:
            # Make a graph for each tree.
            g = Graph(directed=False)
            graphs.append(g)
            g.graph_properties.treeID = g.new_graph_property("string")
            g.graph_properties.inline_svg = g.new_graph_property("string")
            g.vertex_properties.genes = g.new_vertex_property("object")
            g.vertex_properties.label = g.new_vertex_property("string")
            g.vertex_properties.fill_color = g.new_vertex_property("string")

            # set the treeID in the graph properties.
            if root.name == "Root":
                treeID = root.data_members["treeID"]
            elif root.name == "ComOut":
                # grumble. mfm-griddata-parser still isn't type-aware, so these are still strings.
                # TODO: make these ints when parser is fixed.
                treeID = '3'
            elif root.name == "Direction":
                treeID = '1'
            elif root.name == "Movement":
                treeID = '2'

            g.graph_properties.treeID = treeID

            # add the root gene to the graph.
            root_vertex = g.add_vertex()
            g.vertex_properties.genes[int(root_vertex)] = root
            g.vp.label[int(root_vertex)] = 'root: ' + root.name
            g.vp.fill_color[int(root_vertex)] = "xkcd:vomit green"

        for g in graphs:
            # put the rest of the tree genes in each graph
            for atom in self.atoms_in_cell:
                try:
                    if (atom.data_members['treeID'] == g.gp.treeID
                        and atom.name in {"OperatorGene",
                                          "ComIn",
                                          "Value",
                                          "VarRef"}):
                        v = g.add_vertex()
                        g.vp.genes[int(v)] = atom
                        g.vp.label[int(v)] = atom.data_members["geneID"] + ": " + atom.name
                        g.vp.fill_color[int(v)] = "xkcd:ugly purple"
                except KeyError:
                    continue
            # create edges now that all of the genes are in the graph
            for v in g.vertices():
                this_gene = g.vertex_properties.genes[int(v)]

                #operators only:
                if this_gene.name in {"OperatorGene",
                                      "Root",
                                      "ComOut",
                                      "Direction",
                                      "Movement"}:
                    tree0 = this_gene.data_members['tree0']
                    tree1 = this_gene.data_members['tree1']
                    for _v in g.vertices():
                        check_gene = g.vertex_properties.genes[int(_v)]
                        try:
                            if check_gene.data_members['geneID'] in {tree0, tree1}:
                                g.add_edge(v, _v)
                        except KeyError:
                            # root Gene
                            if check_gene.name in {"Root",
                                                   "ComOut",
                                                   "Direction",
                                                   "Movement"}:
                                continue
                            else:
                                raise
            #store the svg as a string on the graph
            svg = BytesIO()

            graph_draw(
                g,
                output=svg,
                fmt='svg',
                output_size=(800,600),
                vprops={'text': g.vertex_properties.label,
                        'fill_color': g.vertex_properties.fill_color,
                        'font_size': 8})
#                        'size': 1})
#                        'pen_width': 1},
#                eprops={'pen_width': 0.8})
            svg.seek(0)
            g.gp.inline_svg = svg.getvalue()
            svg.close()
        
        return graphs
            
            

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

