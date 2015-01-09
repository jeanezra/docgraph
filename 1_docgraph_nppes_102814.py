import pandas as pd
from datetime import datetime

### Data Sources

# Docgraph dataset used
# Source: https://questions.cms.gov/faq.php?id=5005&faqId=7977
# DocGraph-2012-2013-Days30-Edge-Public-Domain/DocGraph-2012-2013-Days30.csv

# NPPES dataset used
# Source: http://nppes.viva-it.com/NPI_Files.html
# npidata_20050523-20141012.csv
# npidata_20050523-20141012FileHeader.csv

# Physician Compare data
# Source: https://data.medicare.gov/data/physician-compare
# National_Downloadable_File.csv



### FUNCTIONS
# Run program
def run():
    start = datetime.now()
    data()
    docgraph_nppes_compare()
    # explore_date()
    extract_state(merge_inner,ny,'NY','ny.txt')
    end = datetime.now()
    elapsed = end - start
    print 'run complete', '| timestamp: ', datetime.now().isoformat(), '| elapsed: ', elapsed


# 1. Data loads
def data():
    docgraph_data()
    nppes_data()
    phys_compare_data()
    print datetime.now().isoformat()
    return docgraph, nppes, phys_compare

# 2. Data merges
def docgraph_nppes_compare(docgraph,nppes,phys_compare):
    prefix_nppes(nppes,'phys_a',nppes_a)
    data_merge(docgraph,nppes_a,phys_compare)
    data_merge2(merge_inner,phys_compare)
    print datetime.now().isoformat()
    return merge_inner, doc_nppes_phys


### Data loads: data() function
# 1a. Docgraph data 2012-2013 - w/in 30 days 'presumed' referral
def docgraph_data():
    docgraph = pd.read_table('DocGraph-2012-2013-Days30.csv',sep=',',index_col=None,header=None)
    print docgraph
    docgraph_col = ['npi_a','npi_b','patient_cnt','unique_patient_cnt','same_day_count']
    docgraph.columns = docgraph_col
    print docgraph.columns
    print datetime.now().isoformat()
    return docgraph

# 1b. NPPES data from October 2014 (npidata_20050523-20141012.csv)
def nppes_data():
    nppes = pd.read_table('npidata_20050523-20141012.csv',sep=',',index_col=None,header=0)
    print nppes
    print datetime.now().isoformat()
    return nppes

# 1c. Physician compare
def phys_compare_data():
    phys_compare = pd.read_table('National_Downloadable_File.csv',sep=',',index_col=None,header=0)
    print phys_compare.columns
    print datetime.now().isoformat()
    return phys_compare


### Data merges: docgraph_nppes(docgraph,nppes) function
# 2a. Add prefix for variables to specify it pertains to physician A
def prefix_nppes(nppes,prefix,nppes_pre):
    nppes_prefix = []
    nppes_col = nppes.columns
    for i in nppes_col:
        col = "%s_%s" % (prefix,i)
        nppes_prefix.append(col)
    nppes_pre = nppes.copy(deep=True)
    nppes_pre.columns = nppes_prefix
    print nppes_pre
    print datetime.now().isoformat()
    return nppes_pre

# 2b. Merge NPPES to Docgraph for physician A
def data_merge(docgraph,nppes_pre):
    merge_inner = pd.merge(docgraph,nppes_pre,how='inner',left_on='npi_a',right_on='phys_a_NPI')
    print merge_inner
    merge_inner.to_csv('docgraph_nppes_a.txt',sep='\t',index=False,header=True)
    # Over 40GB - did not finish was taking more than 24 hours
    print datetime.now().isoformat()
    return merge_inner

# 2c. Merge physician compare to Docgraph/NPPES dataset for physician A
def data_merge2(docgraph_nppes,phys_compare):
    doc_nppes_phys = pd.merge(docgraph_nppes,phys_compare,how='left',on='NPI')
    print doc_nppes_phys
    print datetime.now().isoformat()
    return doc_nppes_phys

# Difference with NPIs in the dataset (Docgraph vs. NPPES)
# 73071804 - 72635381
# 436423


# 3. Explore dataset
def explore(merge_inner):
    print len(merge_inner.columns)
    # 334
    # Show first 40 columns
    print merge_inner.columns[0:40]
    # Identify state variables
    print merge_inner['phys_a_Provider Business Mailing Address State Name'].value_counts()
    print merge_inner['phys_a_Provider Business Practice Location Address State Name'].value_counts()
    # Identify entity type (individual vs. provider organization subpart)
    print merge_inner['phys_a_Entity Type Code'].value_counts()
    print merge_inner['phys_a_NPI Deactivation Reason Code'].value_counts()
    print merge_inner['phys_a_Provider Enumeration Date'].value_counts()
    print merge_inner['phys_a_Last Update Date'].value_counts()
    print merge_inner['phys_a_NPI Deactivation Date'].value_counts()
    print merge_inner['phys_a_NPI Reactivation Date'].value_counts()
    print merge_inner['phys_a_Provider Credential Text'].value_counts()
    print merge_inner['phys_a_Provider Other Organization Name Type Code'].value_counts()
    print datetime.now().isoformat()


# 4. Subset dataset to a state
# Recommendation: Extract top 5 states (FL, CA, NY, TX, PA) + NJ, due to proximity to PA, NY
def extract_state(merge_inner,state,st_abbr,output):
    state = merge_inner[merge_inner['phys_a_Provider Business Practice Location Address State Name'] == st_abbr]
    state.to_csv(output,sep='\t',index=False,header=True)
    print len(state['npi_a'].unique())
    print len(state['npi_b'].unique())
    print datetime.now().isoformat()
    return state





### MAIN CODE
run()