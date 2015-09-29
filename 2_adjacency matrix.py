import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from datetime import datetime
import sys




# 0. Import data
def read_subset(infile):
    subset = pd.read_table(infile,sep='\t',index_col=None,header=0)
    print subset.shape
    return subset



# 1. Create dictionary of npi, and tuples of of source, target, weight
# Pull first 4 columns
def source_target_count(subset):
    subset_edge = subset[['npi_a','npi_b','patient_cnt']]
    print subset_edge.head()
    return subset_edge

# Generate unique NPI list
def unique_npi(subset):
    subset_a = Series(subset['npi_a'].unique())
    subset_b = Series(subset['npi_b'].unique())
    subset_ab = list(Series(pd.concat([subset_a,subset_b],axis=0)).unique())
    print subset_ab
    return subset_ab

# Generate dictionary of NPI to index
def npi_n(subset_ab):
    n = len(subset_ab)
    print n
    # uws: 8580
    # manhattan: 83437
    return n

def npi_index(n,subset_ab):
    index = list(range(0,n))
    print index
    dictionary = dict(zip(subset_ab,index))
    print dictionary
    return dictionary

def npi_edge(subset_edge,dictionary):
    # Replace NPI values with index
    subset_edge['npi_a'].replace(dictionary,inplace=True)
    subset_edge['npi_b'].replace(dictionary,inplace=True)
    print subset_edge.head()
    return subset_edge

def npi_tuples(subset_edge):
    # Create tuples of source, target, weight
    subset = subset_edge[['npi_a','npi_b','patient_cnt']]
    tuples = [tuple(x) for x in subset.values]
    print tuples
    return tuples



# 2. Create adjancency matrix
# Create empty adjacency matrix to fill
def npi_matrix(n):
    matrix = np.array(np.zeros((n,n), int))
    print matrix
    return matrix

# Fill empty adjacency matrix with based on source, target, weight
def matrix_fill(matrix,tuples):
    for a,b,c in tuples:
        matrix[a][b] = c
    return matrix

def matrix_test(matrix):
    print matrix
    print matrix[0][782]
    # 44

# Translate matrix into DataFrame
def matrix_df(matrix):
    df = DataFrame(matrix)
    print df.ix[0][df.columns[782:783]]
    # 44
    return df

# Replace DataFrame columns with target NPI names
def matrix_col_names(subset_ab,df):
    col = []
    for v in subset_ab:
        name = "%s_%s" % ('npi',v)
        col.append(name)
    print col
    df.columns = col
    print df.columns
    return df



# 3. Calculate weight statistics
def weight_stats(df,weightfile):
    df['weight_sum'] = df[df.columns[0:83437]].sum(axis=1)
    df['weight_mean'] = df[df.columns[0:83437]].mean(axis=1)
    df['weight_median'] = df[df.columns[0:83437]].median(axis=1)
    df['weight_min'] = df[df.columns[0:83437]].min(axis=1)
    df['weight_max'] = df[df.columns[0:83437]].max(axis=1)
    df['weight_std'] = df[df.columns[0:83437]].std(axis=1)
    # df['weight_skew'] = df[df.columns[0:83437]].skew(axis=1)
    # df['weight_kurt'] = df[df.columns[0:83437]].kurtosis(axis=1)
    df2 = df.replace(0,np.nan)
    df2['weight_count'] = df2[df2.columns[0:83437]].count(axis=1)
    df = df2.replace(np.nan,0)
    weight_stats = df[df.columns[-7:]]
    weight_stats.to_csv(weightfile,sep='\t',index=False,header=True)



# 4. Export adjacency matrix
def main(infile,outfile,weightfile):
    start =  datetime.now()
    print 'Start: ', start
    subset = read_subset(infile)
    step_0 = datetime.now()
    elapsed = step_0 - start
    print 'step: 0', '| timestamp:', datetime.now().isoformat(), '| time elapsed:', elapsed
    subset_edge = source_target_count(subset)
    subset_ab = unique_npi(subset)
    n = npi_n(subset_ab)
    dictionary = npi_index(n,subset_ab)
    subset_edge = npi_edge(subset_edge,dictionary)
    tuples = npi_tuples(subset_edge)
    step_1 = datetime.now()
    elapsed = step_1 - step_0
    print 'step: 1', '| timestamp:', datetime.now().isoformat(), '| time elapsed:', elapsed
    matrix = npi_matrix(n)
    matrix = matrix_fill(matrix,tuples)
    print matrix_test(matrix)
    df = matrix_df(matrix)
    df = matrix_col_names(subset_ab,df)
    step_2 = datetime.now()
    elapsed = step_2 - step_1
    print 'step: 2', '| timestamp:', datetime.now().isoformat(), '| time elapsed:', elapsed
    df.to_csv(outfile,sep='\t',index=False,header=True)
    weight_stats(df,weightfile)
    step_3 = datetime.now()
    elapsed = step_3 - step_2
    print 'step: 3', '| timestamp:', datetime.now().isoformat(), '| time elapsed:', elapsed
    print 'End: ', datetime.now().isoformat()





### MAIN CODE
if __name__ == "__main__":
    infile = '/home/docgraph/' + sys.argv[1]
    outfile = '/home/docgraph/' + sys.argv[2]
    weightfile = '/home/docgraph/' + sys.argv[3]
    main(infile,outfile,weightfile)

# Add meta data from '3 UWS metadata 110414.py' in shell
# paste -d'\t' uws_adj_mtrx_122214.txt uws_weight_stats_122214.txt uws_easy_meta_120214.txt uws_gephi_stats.txt > uws_122214.txt

# Save script and print out
# python '2 Adjacency matrix 110414.py' > '2 Adjacency matrix 110414.log'