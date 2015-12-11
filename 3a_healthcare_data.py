import pandas as pd
from pandas import Series, DataFrame
import sys
from datetime import datetime



def docgraph_file(infile):
    hood = pd.read_table(infile,sep='\t',index_col=None,header=0,
                         usecols=['npi_a','npi_b'])
    print hood.shape
    return hood

def npi_file():
    npi = pd.read_table('/home/ayasdi/docgraph/npidata_20050523-20141012.csv',sep=',',index_col=None,header=0,
                        usecols=['NPI',
                                 'Healthcare Provider Taxonomy Code_1',
                                 'Is Sole Proprietor',
                                 'Is Organization Subpart']
    )
    print npi.shape
    return npi

# Specialty taxonomy to get description of specialty code
def nucc_file():
    nucc = pd.read_table('/home/ayasdi/docgraph/nucc_taxonomy_141.csv',sep=',',index_col=None,header=0,
                         usecols=['Code','Classification'])
    print nucc.shape
    return nucc

# Find metadata for both physician A and B
def npi_unique(hood):
    phys_a = Series(hood['npi_a'])
    phys_b = Series(hood['npi_b'])
    phys_ab = pd.concat([phys_a,phys_b],axis=0)
    print len(phys_ab)
    phys_unq = DataFrame(phys_ab.unique())
    phys_unq.columns = ['npi']
    print len(phys_unq)
    return phys_unq

# Pull npi rows associated with neighborhood
def npi_unique_data(phys_unq,npi):
    phys_npi = pd.merge(phys_unq,npi,how='left',left_on='npi',right_on='NPI')
    print phys_npi.shape
    return phys_npi

# Merge specialty description to npi subset
def phys_npi_nucc(phys_npi,nucc):
    npi_nucc = pd.merge(phys_npi,nucc,how='left',left_on='Healthcare Provider Taxonomy Code_1',right_on='Code')
    print npi_nucc.shape
    return npi_nucc

# Add in additional data (physician compare; physician payment & utilization)
# def compare_file():
#     phys_compare = pd.read_table('National_Downloadable_File.csv',sep=',',index_col=None,header=0)
#     print phys_compare.shape
#     return phys_compare

# def npi_nucc_compare(npi_nucc,phys_compare):
#     uws_compare = pd.merge(npi_nucc,phys_compare,how='left',on='NPI')
#     print uws_compare.shape
#     return uws_compare

# def mppu_file():
#     mppu = pd.read_table('mppu.txt',sep='\t',index_col=None,header=0)
#     print mppu.shape
#     return mppu
# There will be duplicate rows - unstack to get each procedure code on the same row - already done?

# def npi_source(npi_nucc,hood):
#     hood_npi_a = pd.merge(hood,npi_nucc,how='left',left_on='npi_a',right_on='NPI')
#     print hood_npi_a.shape
#     return hood_npi_a
#
# def npi_target(hood_npi_a,hood):
#     hood_npi_b = pd.merge(hood,hood_npi_a,how='left',left_on='npi_b',right_on='NPI')
#     print hood_npi_b.shape
#     return hood_npi_b

# npi_nucc['Provider Gender - Male'] = npi_nucc['Provider Gender Code'].apply(lambda x: 1 if x == 'M' else 0)
# npi_nucc['Provider Gender - Female'] = npi_nucc['Provider Gender Code'].apply(lambda x: 1 if x == 'F' else 0)

def basic_dummies(npi_nucc):
    specialty = pd.get_dummies(npi_nucc['Classification'],prefix='specialty')
    print specialty.shape
    sole_prop = pd.get_dummies(npi_nucc['Is Sole Proprietor'],prefix='sole_proprietor')
    print sole_prop.shape
    org_subpart = pd.get_dummies(npi_nucc['Is Organization Subpart'],prefix='org_subpart')
    print org_subpart.shape
    dum = pd.concat([specialty,sole_prop,org_subpart],axis=1)
    print dum.shape
    return dum

def source_sort(npi_nucc_dum,key):
    source_key = pd.read_table(key,sep='\t',header=0,usecols=['source'])
    sorted = pd.merge(source_key,npi_nucc_dum,how='inner',left_on='source',right_on='npi')
    print sorted.shape
    return sorted

def main(infile,key,outfile):
    start = datetime.now()
    print 'Start: ', start
    hood = docgraph_file(infile)
    phys_unq = npi_unique(hood)
    npi = npi_file()
    phys_npi = npi_unique_data(phys_unq,npi)
    nucc = nucc_file()
    npi_nucc = phys_npi_nucc(phys_npi,nucc)
    # hood_npi_a = npi_source(npi_nucc,hood)
    # hood_npi_b = npi_target(hood_npi_a,hood)
    dum = basic_dummies(npi_nucc)
    npi_nucc_dum = pd.concat([npi_nucc,dum],axis=1)
    print npi_nucc_dum.shape
    sorted = source_sort(npi_nucc_dum,key)
    sorted.to_csv(outfile,sep='\t',index=False,header=True)
    end = datetime.now()
    print 'End: ', end
    elapsed = end - start
    print 'Time elapsed:', elapsed



if __name__ == '__main__':
    infile = '/home/ayasdi/docgraph/' + sys.argv[1]
    key = '/home/ayasdi/docgraph/' + sys.argv[2]
    outfile = '/home/ayasdi/docgraph/' + sys.argv[3]
    main(infile,key,outfile)