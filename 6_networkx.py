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

def adj_matrix(graph):
    adj_mtrx = nx.adjacency_matrix(graph,weight='weight')
    print adj_mtrx
    return adj_mtrx

def adj_matrix_df(adj_mtrx):
    adj_df = DataFrame(adj_mtrx.todense())
    print adj_df.shape
    return adj_df

def adj_matrix_col(graph,adj_df):
    col_name = graph.nodes()
    prefixed = []
    for i in col_name:
        prefix = "%s_%s" % ('npi',i)
        prefixed.append(prefix)
    print prefixed
    adj_df.columns = prefixed
    return adj_df

def main(infile):
    start = datetime.now()
    print 'Start: ', start
    graph = read_data(infile)
    adj_mtrx = adj_matrix(graph)
    adj_df = adj_matrix_df(adj_mtrx)
    graph_col = adj_matrix_col(graph,adj_df)
    graph_col.to_csv('uws_adj_mtrx.txt',sep='\t',index=False,header=True)
    end = datetime.now()
    print 'End: ', end
    elapsed = end - start
    print 'Time elapsed:', elapsed



### MAIN CODE
if __name__ == "__main__":
    infile = '/home/ayasdi/docgraph/' + sys.argv[1]
    # uws_weighted_edgelist_nohead.txt
    main(infile)
