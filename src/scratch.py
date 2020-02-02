from mfm_emm_graph.grid import Grid

g = Grid('/home/sharmon/git-repos/mfm-datastring-parser/tests/file1.save')
cell0 = g.cells[0]
for graph in cell0.tree_graphs:
    for v in graph.vertices():
        print(int(v))
        print(graph.vp.genes[int(v)].name + str(graph.vp.genes[int(v)].data_members))
    
