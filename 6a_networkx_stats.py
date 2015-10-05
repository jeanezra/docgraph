# Create edge list
# cut -d$'\t' -f 1-3 uws.txt > uws_weighted_edgelist.txt
# scp white:~/docgraph/uws_weighted_edgelist.txt .
# cat uws_weighted_edgelist.txt | sed "1 d" > uws_weighted_edgelist_nohead.txt
import networkx as nx
from pandas import DataFrame
import sys
from datetime import datetime



### FUNCTIONS
def read_data(infile):
    graph = nx.read_weighted_edgelist(infile,delimiter='\t',nodetype=str,create_using=nx.DiGraph())
    print graph
    return graph

def calc_degree(graph):
    degree = nx.degree_centrality(graph)
    print degree
    return degree

def dict_to_df(dictionary):
    df = DataFrame(dictionary.items(), columns=['source','degree_centrality'])
    print df.shape
    return df

def main(infile):
    start = datetime.now()
    print 'Start: ', start
    graph = read_data(infile)
    degree = calc_degree(graph)
    df = dict_to_df(degree)
    df.to_csv('uws_adj_mtrx.txt',sep='\t',index=False,header=True)
    end = datetime.now()
    print 'End: ', end
    elapsed = end - start
    print 'Time elapsed:', elapsed



### MAIN CODE
if __name__ == "__main__":
    infile = '/home/ayasdi/docgraph/' + sys.argv[1]
    # uws_weighted_edgelist_nohead.txt
    main(infile)
