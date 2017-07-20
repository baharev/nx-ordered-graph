# Copyright (C) 2016, 2017 University of Vienna
# All rights reserved.
# BSD license.
# Author: Ali Baharev <ali.baharev@gmail.com>
from __future__ import print_function, division
import os
from hypothesis import given, settings
from hypothesis.strategies import integers
from networkx import OrderedDiGraph, gnm_random_graph

class MyOrderedDiGraph(OrderedDiGraph):
    
    #@profile
    def subgraph(self, nbunch):
        bunch = self.nbunch_iter(nbunch)
        # create new graph and copy subgraph into it
        H = self.__class__()
        # copy node and attribute dictionaries
        for n in bunch:
            H.node[n]=self.node[n]
        # namespace shortcuts for speed
        H_succ=H.succ
        H_pred=H.pred
        self_succ=self.succ
        self_pred=self.pred
        # add nodes
        for n in H:
            H_succ[n]=H.adjlist_inner_dict_factory()
            H_pred[n]=H.adjlist_inner_dict_factory()
        # add successors
        for u in H_succ:
            Hnbrs=H_succ[u]
            for v,datadict in self_succ[u].items():
                if v in H_succ:
                    Hnbrs[v]=datadict
        # add predecessors
        for u in H_pred:
            Hnbrs=H_pred[u]
            for v,datadict in self_pred[u].items():
                if v in H_pred:
                    Hnbrs[v]=datadict
        H.graph=self.graph
        return H

#def check_proxy(n, m, seed):
#    check_order(n, m, seed)

#@profile
def check_order(n, m, seed):
    g_rnd = gnm_random_graph(n, m, seed=seed, directed=True)
    
    g_orig = MyOrderedDiGraph()
    g_orig.add_edges_from(g_rnd.edges())
    g_orig.add_nodes_from(g_rnd.nodes())

    nodes = list(g_orig.nodes())
    
    # still a caveat: must preserve the relative order of the nodes
    g_sub = g_orig.subgraph(nodes)

    for n_orig, n_sub in zip(g_orig, g_sub):
        assert n_orig == n_sub
         
    for e_orig, e_sub in zip(g_orig.edges(), g_sub.edges()):
        assert e_orig == e_sub

    for n in nodes:
        assert list(g_orig.predecessors(n)) == list(g_sub.predecessors(n))
        assert list(g_orig.successors(n))   == list(g_sub.successors(n))
        
    #print('nodes: %d, edges: %d' % (g_orig.number_of_nodes(), g_orig.number_of_edges()))  


def main():
    print('Started generative testing...')
    os.environ['HYPOTHESIS_STORAGE_DIRECTORY'] = '/tmp/ht'
    
    MAX_VALUE = 30
    
    with settings(max_examples=10000):
        decor = given(n    = integers(min_value=0, max_value=  MAX_VALUE),
                      m    = integers(min_value=0, max_value=5*MAX_VALUE), 
                      seed = integers(min_value=1))
        
        decor(check_order)()
    
    print('Done!')


if __name__ == '__main__':
    import networkx
    import hypothesis
    print('networkx', networkx.__version__)
    print('hypothesis', hypothesis.__version__)
    main()
