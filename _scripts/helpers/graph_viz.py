import networkx as nx

def draw_planar(G):
    pos=nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True)
    return pos

def draw_spectral(G):
    nx.draw_spectral(G, with_labels=True)

def draw_spring(G):
    pos=nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    return pos
