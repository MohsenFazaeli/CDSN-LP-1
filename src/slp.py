import networkx as nx
import random
from tqdm import tqdm
from community import modularity
from calculation_helper import overlap, unit, min_norm, normalized_overlap,  overlap_generator
from graph_io import json_dumper

class LabelPropagator:

    def __init__(self, graph, args):

        """
        """
        self.args = args
        self.seeding = args.seed
        self.graph = graph
        self.nodes = graph.nodes()
        self.rounds = args.rounds
        self.labels = {node: node for node in self.nodes}
        self.label_count = len(set(self.labels.values()))
        self.flag = True
        self.weight_setup(args.weighting)

    def weight_setup(self, weighting):
        """
        """

        if weighting == "overlap":
            self.weights  = overlap_generator(overlap, self.graph)
        elif weighting == "unit":
            self.weights  = overlap_generator(unit, self.graph)
        elif weighting == "min_norm":
            self.weights  = overlap_generator(min_norm, self.graph)
        else:
            self.weights  = overlap_generator(normalized_overlap, self.graph)

    def make_a_pick(self, source, neighbors):
        """
        """

        scores = {}
        for neighbor in neighbors:
            neighbor_label = self.labels[neighbor]
            if neighbor_label in scores.keys():
                scores[neighbor_label] = scores[neighbor_label] +  self.weights[(neighbor,source)]
            else:
                scores[neighbor_label] = self.weights[(neighbor,source)]
        top = [key for key,val in scores.iteritems() if val == max(scores.values())]
        return random.sample(top,1)[0]

    def do_a_propagation(self):
        """
        """
        random.seed(self.seeding)
        random.shuffle(self.nodes)
        for node in tqdm(self.nodes):
             neighbors = nx.neighbors(self.graph, node)
             pick = self.make_a_pick(node, neighbors)
             self.labels[node] = pick
        current_label_count = len(set(self.labels.values()))
        if self.label_count == current_label_count:
            self.flag = False
        else:
            self.label_count = current_label_count



    def do_a_series_of_propagations(self):
        index = 0
        while index < self.rounds and self.flag:
            index = index + 1
            print("Label propagation round: " + str(index))
            self.do_a_propagation()
        print("")
        print("Modularity is: "+  str(round(modularity(self.labels,self.graph),3)) + ".")
        json_dumper(self.labels, self.args.assignment_output)

