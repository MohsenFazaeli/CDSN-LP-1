from parser import parameter_parser
from model import LabelPropagator
from graph_io import graph_reader
from matplotlib import pyplot as plt
import networkx as nx
from jupyterthemes import jtplot
import random
from tqdm import tqdm
from graph_io import json_dumper
from community import modularity




def make_a_pick(G, source, neighbors):
    """
    here we pick one community to repeat but we change our pick strategy to dont pick our enemy choice
    """

    scores = {}
    for neighbor in neighbors:
        #print str(source)+" neighbor is: "
        #print G[2]
        #print [n for n in neighbors]
        neighbor_label = G.nodes[neighbor]['poslabel']
        if neighbor_label in scores.keys():
            scores[neighbor_label] = scores[neighbor_label] + G[source][neighbor]['weight']
        else:
            scores[neighbor_label] = G[source][neighbor]['weight']
    top = [key for key, val in scores.iteritems() if val == max(scores.values())]
    return random.sample(top, 1)[0]


def do_a_propagation(G):
    """
    """
    random.seed(1)
    #print G.nodes()
    p=[i for i in G.nodes()]
    random.shuffle(p)
    for node in tqdm(p):
        neighbors = G.neighbors(node)

        #print [n for n in neighbors]
        #print type(neighbors)
        #print neighbors[2]
        #print neighbors[2]
        #print neighbors[2]

        pick = make_a_pick(G,node, neighbors)
        G.nodes[node]['poslabel'] = pick
    #current_label_count = len(set(self.labels.values()))
    #if self.label_count == current_label_count:
    #    self.flag = False
    #else:
    #    self.label_count = current_label_count


def do_a_series_of_propagations(G):
    index = 0
    while index < 10 :
        index = index + 1
        print("Label propagation round: " + str(index))
        do_a_propagation(G)
    print("")
    #print("Modularity is: " + str(round(modularity(self.labels, self.graph), 3)) + ".")
    #json_dumper(self.labels, self.args.assignment_output)


def create_and_run_model(args):
    G = graph_reader(args.input)
    #print G.nodes

    labels = {i: {'poslabel': i, 'negLabels': -1} for i in G.nodes}
    #print labels
    nx.set_node_attributes(G, labels)
    #print G.nodes[1]['poslabel']
    #print G.nodes[1]['poslabel']
    #print G.nodes[1]['poslabel']
    #print G.nodes[1]['negLabels']
    #print G.nodes[1]['negLabels']
    do_a_series_of_propagations(G)
    for node in G.nodes:
        print str(node)+"->"+str(G.nodes[node]['poslabel'])


    """
    edges, edges_color = zip(*nx.get_edge_attributes(G, 'color').items())
    print edges_color
    val_map = {6: 1.0, 13: 0.5714285714285714, 16: 0.0} #tribe
    val_map = {7: 1.0, 13: 0.5714285714285714, 8: 0.0} #tribe


    # print type(val_map)
    # print G.nodes()
    #print [G.nodes[node]['poslabel'] for node in G.nodes()]

    values = [val_map.get(node, 0.25) for node in G.nodes()]
    values = [val_map.get(G.nodes[node]['poslabel'], 0.25) for node in G.nodes()]
    print values

    pos = nx.spring_layout(G, iterations=200)
    #pos = nx.spectral_layout(G,weight='weight')
    #tribes pos = nx.shell_layout(G,[[3,4,6,7,8,11,12],[1,2,15,16],[5,9,10,13,14]])
    pos = nx.shell_layout(G,[[1,2,6,8,9],[3,4,5,7,10]]) #stranke94
    nx.draw_networkx(G,pos, cmap=plt.get_cmap('jet'), node_color=values, edge_color=edges_color)
    plt.show()
"""
    #calculalate q signed
    wt_p = 0 #total posetive weights
    for (u, v, c) in G.edges.data('weight', default=0):
        wt_p += c if c > 0 else 0
        #wt_p += 1 if c > 0 else 0
    print wt_p

    wt_n = 0
    for (u, v, c) in G.edges.data('weight', default=0):
        wt_n += c*-1 if c < 0 else 0
        #wt_n += 1 if c < 0 else 0
    print wt_n

    print [n for n in G.neighbors(1)]
    print [n for n in G.neighbors(2)]
    print [n for n in G.neighbors(3)]
    print [n for n in G.neighbors(4)]

    w_p = {n: 0 for n in G.nodes}
    w_n = {n: 0 for n in G.nodes}

    for wi in G.nodes():
        for wj in G.neighbors(wi):
            if G.edges[wi, wj]['weight'] > 0:
                w_p[wi] += G.edges[wi, wj]['weight']
                #w_p[wi] += 1
            else:
                if(G.edges[wi, wj]['weight'] != 0):
                    w_n[wi] -= G.edges[wi, wj]['weight']
                    #w_n[wi] += 1

    sum = 0

    for wi in G.nodes():
        for wj in G.neighbors(wi):
            if (G.nodes[wi]['poslabel'] == G.nodes[wj]['poslabel']):
                sum += G.edges[wi, wj]['weight'] - \
                       ((w_p[wi] * 1.0 * w_p[wj]) / (2.0 * wt_p) - (w_p[wi] * 1.0 * w_p[wj]) / (2.0 * wt_n))

    normfacto=1.0/(2.0*(wt_p+wt_n))

    print "final Q singed is:" + str (normfacto*sum)




if __name__ == "__main__":
    args = parameter_parser()
    create_and_run_model(args)
    #do_a_series_of_propagations()
