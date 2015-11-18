import networkx as nx
import pandas as pd
from pandas import DataFrame
import sys
from datetime import datetime



### FUNCTIONS
def read_data(infile):
    graph = nx.read_weighted_edgelist(infile,delimiter='\t',nodetype=str,create_using=nx.DiGraph())
    print graph
    return graph

# Degree (overall, in, out - expressed as proportions, where denominator is the number of nodes in dataset)
def calc_degree(graph):
    degree = nx.degree_centrality(graph)
    print degree
    return degree

def calc_indegree(graph):
    indegree = nx.in_degree_centrality(graph)
    print indegree
    return indegree

def calc_outdegree(graph):
    outdegree = nx.out_degree_centrality(graph)
    print outdegree
    return outdegree

# Closeness
def calc_closeness(graph):
    closeness = nx.closeness_centrality(graph,normalized=True)
    print closeness
    return closeness

# Betweenness
# for nodes
def calc_betweenness(graph):
    betweenness = nx.betweenness_centrality(graph,normalized=True)
    print betweenness
    return betweenness

# # for edges
# def calc_edge_betweenness(graph):
#     edge_betweenness = nx.edge_betweenness_centrality(graph,normalized=True)
#     print edge_betweenness
#     return edge_betweenness


# Convert to DataFrame format
def dict_to_df(dictionary,col_name):
    df = DataFrame(dictionary.items(), columns=['source',col_name])
    df.set_index('source',inplace=True)
    print df.shape
    return df

def sna_agg(degree,indegree,outdegree,closeness,betweenness):
    calculations = [degree,indegree,outdegree,closeness,betweenness]
    col_name = ['degree','indegree','outdegree','closeness','betweenness']
    dict = {}
    for i,j in zip(calculations,col_name):
        dict[j] = dict_to_df(i,j)
    print len(dict)
    df = dict['degree'].join([dict['indegree'],dict['outdegree'],dict['closeness'],dict['betweenness']],how='inner')
    print df.head(), '\n', df.tail()
    return df

def main(infile,outfile):
    start = datetime.now()
    print 'Start: ', start
    graph = read_data(infile)
    degree = calc_degree(graph)
    indegree = calc_indegree(graph)
    outdegree = calc_outdegree(graph)
    closeness = calc_closeness(graph)
    betweenness = calc_betweenness(graph)
    df = sna_agg(degree,indegree,outdegree,closeness,betweenness)
    df.to_csv(outfile,sep='\t',index=True,header=True)
    end = datetime.now()
    print 'End: ', end
    elapsed = end - start
    print 'Time elapsed:', elapsed



### MAIN CODE
if __name__ == "__main__":
    infile = '/home/ayasdi/docgraph/' + sys.argv[1]
    # uws_weighted_edgelist_nohead.txt
    outfile = '/home/ayasdi/docgraph/' + sys.argv[2]
    main(infile,outfile)
