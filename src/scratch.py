from mfm_emm_graph.grid import Grid
from graph_tool.all import graph_draw

g = Grid('/home/spencer/git-repos/mfm-griddata-parser/tests/file1.save')
cell0 = g.cells[0]
graph1 = cell0.tree_graphs[1]
print(graph1.vertex_index.__dict__)
graph_draw(graph1, vprops={'text': graph1.vertex_properties.label})
#graph_draw(graph1, vprops={'text': graph1.vertex_index})
for graph in cell0.tree_graphs:
    for v in graph.vertices():
        print(int(v))
        print(graph.vp.genes[int(v)].name + str(graph.vp.genes[int(v)].data_members))
    
