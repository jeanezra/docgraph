import pandas as pd
import numpy as np
from datetime import datetime

infile = '/home/ayasdi/docgraph/manhattan_adj_mtrx_092815.txt'
# infile = '/home/ayasdi/docgraph/manhattan_test.txt'

weightfile = '/home/ayasdi/docgraph/manhattan_weight_stats_092915.txt'
# weightfile = '/home/ayasdi/docgraph/manhattan_test_out.txt'

df = pd.read_table(infile,sep='\t',index_col=False,header=0,chunksize=1000)

print 'Start: ', datetime.now().isoformat()
# 3. Calculate weight statistics
i = 1
for chunk in df:
    print i, datetime.now().isoformat()
    # print chunk.shape
    chunk['weight_sum'] = chunk[chunk.columns[0:83437]].sum(axis=1)
    chunk['weight_mean'] = chunk[chunk.columns[0:83437]].mean(axis=1)
    chunk['weight_median'] = chunk[chunk.columns[0:83437]].median(axis=1)
    chunk['weight_min'] = chunk[chunk.columns[0:83437]].min(axis=1)
    chunk['weight_max'] = chunk[chunk.columns[0:83437]].max(axis=1)
    chunk['weight_std'] = chunk[chunk.columns[0:83437]].std(axis=1)
    # chunk['weight_skew'] = chunk[chunk.columns[0:83437]].skew(axis=1)
    # chunk['weight_kurt'] = chunk[chunk.columns[0:83437]].kurtosis(axis=1)
    chunk2 = chunk.replace(0,np.nan)
    # print chunk2.shape
    chunk2['weight_count'] = chunk2[chunk2.columns[0:83437]].count(axis=1)
    chunk = chunk2.replace(np.nan,0)
    # print chunk.shape
    weight_stats = chunk[chunk.columns[-7:]]
    # print weight_stats.shape
    if i == 1:
        weight_stats.to_csv(weightfile,sep='\t',mode='w',index=False,header=True)
    else:
        weight_stats.to_csv(weightfile,sep='\t',mode='a',index=False,header=False)
    i += 1

print 'End: ', datetime.now().isoformat()
