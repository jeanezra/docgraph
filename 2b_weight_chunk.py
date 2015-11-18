import pandas as pd
import numpy as np
from datetime import datetime
import sys


### FUNCTIONS
def read_data(infile):
    df = pd.read_table(infile,sep='\t',index_col=False,header=0,chunksize=1000)
    return df

def weight_compute(df,weightfile):
    df_test = pd.read_table(infile,sep='\t',index_col=False,header=0,nrows=1)
    print df_test.shape
    col_length = len(df_test.columns)
    i = 1
    for chunk in df:
        print i, datetime.now().isoformat()
        chunk['weight_sum'] = chunk[chunk.columns[0:col_length]].sum(axis=1)
        chunk['weight_mean'] = chunk[chunk.columns[0:col_length]].mean(axis=1)
        chunk['weight_median'] = chunk[chunk.columns[0:col_length]].median(axis=1)
        chunk['weight_min'] = chunk[chunk.columns[0:col_length]].min(axis=1)
        chunk['weight_max'] = chunk[chunk.columns[0:col_length]].max(axis=1)
        chunk['weight_std'] = chunk[chunk.columns[0:col_length]].std(axis=1)
        # chunk['weight_skew'] = chunk[chunk.columns[0:col_length]].skew(axis=1)
        # chunk['weight_kurt'] = chunk[chunk.columns[0:col_length]].kurtosis(axis=1)
        chunk2 = chunk.replace(0,np.nan)
        chunk2['weight_count'] = chunk2[chunk2.columns[0:col_length]].count(axis=1)
        chunk3 = chunk2.replace(np.nan,0)
        weight_stats = chunk3[chunk3.columns[-7:]]
        print weight_stats.describe()
        if i == 1:
            weight_stats.to_csv(weightfile,sep='\t',mode='w',index=False,header=True)
        else:
            weight_stats.to_csv(weightfile,sep='\t',mode='a',index=False,header=False)
        i += 1

def main(infile,weightfile):
    print 'Start: ', datetime.now().isoformat()
    df = read_data(infile)
    weight_compute(df,weightfile)
    print 'End: ', datetime.now().isoformat()



### MAIN CODE
if __name__ == "__main__":
    infile = '/home/ayasdi/docgraph/' + sys.argv[1]
    weightfile = '/home/ayasdi/docgraph/' + sys.argv[2]
    main(infile,weightfile)