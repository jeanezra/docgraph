import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from datetime import datetime

start = datetime.now()
print datetime.now().isoformat()

# 0. Import data
uws = pd.read_table('uws.txt',sep='\t',index_col=None,header=0)
step_0 = datetime.now()
elapsed = step_0 - start
print 'step: 0', '| timestamp:', datetime.now().isoformat(), '| time elapsed:', elapsed



# 1. Create dictionary of npi, and tuples of of source, target, weight
# Pull first 4 columns
uws_edge = uws[['npi_a','npi_b','patient_cnt']]
print uws_edge.head()

# Generate unique NPI list
uws_a = Series(uws['npi_a'].unique())
uws_b = Series(uws['npi_b'].unique())
uws_ab = list(Series(pd.concat([uws_a,uws_b],axis=0)).unique())
print uws_ab

# Generate dictionary of NPI to index
n = len(uws_ab)
print n
# 8580
index = list(range(0,n))
print index

dictionary = dict(zip(uws_ab,index))
print dictionary

# Replace NPI values with index
uws_edge['npi_a'].replace(dictionary,inplace=True)
uws_edge['npi_b'].replace(dictionary,inplace=True)
print uws_edge.head()

# Create tuples of source, target, weight
subset = uws_edge[['npi_a','npi_b','patient_cnt']]
tuples = [tuple(x) for x in subset.values]
print tuples

step_1 = datetime.now()
elapsed = step_1 - step_0
print 'step: 1', '| timestamp:', datetime.now().isoformat(), '| time elapsed:', elapsed



# 2. Create adjancency matrix
# Create empty adjacency matrix to fill
matrix = np.array(np.zeros((n,n), int))
print matrix

# Fill empty adjacency matrix with based on source, target, weight
for a,b,c in tuples:
    matrix[a][b] = c

print matrix
print matrix[0][782]
# 44

# Translate matrix into DataFrame
df = DataFrame(matrix)
print df.ix[0][df.columns[782:783]]
# 44

# Replace DataFrame columns with target NPI names
col = []
for v in uws_ab:
    name = "%s_%s" % ('npi',v)
    col.append(name)

print col

df.columns = col
print df.columns

# Export adjacency matrix
df.to_csv('uws_adj_mtrx_122214.txt',sep='\t',index=False,header=True)

step_2 = datetime.now()
elapsed = step_2 - step_1
print 'step: 2', '| timestamp:', datetime.now().isoformat(), '| time elapsed:', elapsed



# 3. Calculate weight statistics
df['weight_sum'] = df[df.columns[0:8580]].sum(axis=1)
df['weight_mean'] = df[df.columns[0:8580]].mean(axis=1)
df['weight_median'] = df[df.columns[0:8580]].median(axis=1)
df['weight_min'] = df[df.columns[0:8580]].min(axis=1)
df['weight_max'] = df[df.columns[0:8580]].max(axis=1)
df['weight_std'] = df[df.columns[0:8580]].std(axis=1)
df['weight_skew'] = df[df.columns[0:8580]].skew(axis=1)
df['weight_kurt'] = df[df.columns[0:8580]].kurtosis(axis=1)
df2 = df.replace(0,np.nan)
df2['weight_count'] = df2[df2.columns[0:8580]].count(axis=1)
df = df2.replace(np.nan,0)

weight_stats = df[df.columns[-9:]]

weight_stats.to_csv('uws_weight_stats_122414.txt',sep='\t',index=False,header=True)

step_3 = datetime.now()
elapsed = step_3 - step_2
print 'step: 3', '| timestamp:', datetime.now().isoformat(), '| time elapsed:', elapsed

# Add meta data from '3 UWS metadata 110414.py' in shell
# paste -d'\t' uws_adj_mtrx_122214.txt uws_weight_stats_122214.txt uws_easy_meta_120214.txt uws_gephi_stats.txt > uws_122214.txt



# Save script and print out
# python '2 Adjacency matrix 110414.py' > '2 Adjacency matrix 110414.log'