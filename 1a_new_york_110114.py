import pandas as pd
from pandas import DataFrame
from datetime import datetime

### Shell commands to create file for Gephi
# Take first 2 columns (Source, Target)
# cut -d$'\t' -f 1-2 uws.txt > uws_2.txt
# Change separation by commas instead of tabs
# cat uws_2.txt | tr '\t' ',' > uws_2.csv
# Remove header
# cat uws_2.csv | sed "1 d" > uws_2_nohead.csv
# Add correct header
# cat header.csv uws_2_nohead.csv > uws_gephi.csv
# Verify file is okay
# head uws_gephi.csv
# Import into Gephi!

print datetime.now().isoformat()

ny = pd.read_table('ny.txt',sep='\t',index_col=None,header=0)
print ny
print datetime.now().isoformat()
print ny.columns
print ny['phys_a_Provider Business Practice Location Address Postal Code'].value_counts()

# Check field lengths
print ny['phys_a_Provider Business Practice Location Address Postal Code'].dtype
print ny['phys_a_Provider Business Practice Location Address Postal Code'].apply(lambda x: len(str(int(x)))).value_counts()

postal4 = ny[ny['phys_a_Provider Business Practice Location Address Postal Code'].apply(lambda x: len(str(int(x)))) == 4]
print postal4['phys_a_Provider Business Practice Location Address Postal Code']
# e.g. 3102 is the ZIP 4 (last 4 digits of the 9 digit zip code)
# 9 digit ZIP code: 13416-3102
postal4_unq = postal4['phys_a_Provider Business Practice Location Address Postal Code'].unique()
print len(postal4_unq)
# 6
postal8 = ny[ny['phys_a_Provider Business Practice Location Address Postal Code'].apply(lambda x: len(str(int(x)))) == 8]
print postal8['phys_a_Provider Business Practice Location Address Postal Code']
# ??? Don't know why there are 8 digits
postal8_unq = postal8['phys_a_Provider Business Practice Location Address Postal Code'].unique()
print len(postal8_unq)
# 1

# Retain records with 5 or 9 digits
postal5 = ny[ny['phys_a_Provider Business Practice Location Address Postal Code'].apply(lambda x: len(str(int(x)))) == 5]
postal9 = ny[ny['phys_a_Provider Business Practice Location Address Postal Code'].apply(lambda x: len(str(int(x)))) == 9]
ny_postal = pd.concat([postal5,postal9],axis=0)
print ny_postal
print datetime.now().isoformat()

# Verify reduced dataset is correct
# 4543442-4544276
# -834



# Take first 5 digits
ny_postal['zip_code_5'] = ny_postal['phys_a_Provider Business Practice Location Address Postal Code'].apply(lambda x: int(str(int(x))[0:5]))
print ny_postal['zip_code_5']
print ny_postal['zip_code_5'].apply(lambda x: len(str(x))).value_counts()
# 5    4543442

# NYC zip codes (http://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm)
nyc = [
10453, 10457, 10460,
10458, 10467, 10468,
10451, 10452, 10456,
10454, 10455, 10459, 10474,
10463, 10471,
10466, 10469, 10470, 10475,
10461, 10462, 10464, 10465, 10472, 10473,
11212, 11213, 11216, 11233, 11238,
11209, 11214, 11228,
11204, 11218, 11219, 11230,
11234, 11236, 11239,
11223, 11224, 11229, 11235,
11201, 11205, 11215, 11217, 11231,
11203, 11210, 11225, 11226,
11207, 11208,
11211, 11222,
11220, 11232,
11206, 11221, 11237,
10026, 10027, 10030, 10037, 10039,
10001, 10011, 10018, 10019, 10020, 10036,
10029, 10035,
10010, 10016, 10017, 10022,
10012, 10013, 10014,
10004, 10005, 10006, 10007, 10038, 10280,
10002, 10003, 10009,
10021, 10028, 10044, 10128,
10023, 10024, 10025,
10031, 10032, 10033, 10034, 10040,
11361, 11362, 11363, 11364,
11354, 11355, 11356, 11357, 11358, 11359, 11360,
11365, 11366, 11367,
11412, 11423, 11432, 11433, 11434, 11435, 11436,
11101, 11102, 11103, 11104, 11105, 11106,
11374, 11375, 11379, 11385,
11691, 11692, 11693, 11694, 11695, 11697,
11004, 11005, 11411, 11413, 11422, 11426, 11427, 11428, 11429,
11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421,
11368, 11369, 11370, 11372, 11373, 11377, 11378,
10302, 10303, 10310,
10306, 10307, 10308, 10309, 10312,
10301, 10304, 10305,
10314
]

manhattan = [
10026, 10027, 10030, 10037, 10039,
10001, 10011, 10018, 10019, 10020, 10036,
10029, 10035,
10010, 10016, 10017, 10022,
10012, 10013, 10014,
10004, 10005, 10006, 10007, 10038, 10280,
10002, 10003, 10009,
10021, 10028, 10044, 10128,
10023, 10024, 10025,
10031, 10032, 10033, 10034, 10040
]

low_manh = [
10001, 10011, 10018, 10019, 10020, 10036,
10010, 10016, 10017, 10022,
10012, 10013, 10014,
10004, 10005, 10006, 10007, 10038, 10280,
10002, 10003, 10009
]

uws = [
10023, 10024, 10025
]

# Filter dataset to New York City
nyc = ny_postal[ny_postal['zip_code_5'].isin(nyc)]
print nyc

manh = ny_postal[ny_postal['zip_code_5'].isin(manhattan)]
print manh

low_manh = ny_postal[ny_postal['zip_code_5'].isin(low_manh)]
print low_manh

uws = ny_postal[ny_postal['zip_code_5'].isin(uws)]
print uws

# Export dataset
nyc.to_csv('nyc.txt',sep='\t',index=False,header=True)
manh.to_csv('manhattan.txt',sep='\t',index=False,header=True)
low_manh.to_csv('low_manhattan.txt',sep='\t',index=False,header=True)
uws.to_csv('uws.txt',sep='\t',index=False,header=True)



nucc = pd.read_table('nucc_taxonomy_141.csv',sep=',',index_col=None,header=0)
print nucc

# Merge in Provider Taxonomy Descriptions
nyc_nucc = pd.merge(nyc,nucc,how='inner',left_on='phys_a_Healthcare Provider Taxonomy Code_1',right_on='Code')
print nyc_nucc
print nyc_nucc['Type'].value_counts()
print nyc_nucc['Classification'].value_counts()





# Create JSON file for D3 visualization
# Create node list first
nyc_a = uws['npi_a']
nyc_b = uws['npi_b']
nyc_ab = pd.concat([nyc_a,nyc_b],axis=0)
print nyc_ab
nyc_ab_df = DataFrame(nyc_ab.unique())
ab_col = ['name']
nyc_ab_df.columns = ab_col
nyc_ab_df['group'] = 1
nyc_nodes_json = nyc_ab_df.to_json(orient='records')

# Find unique (index is reset by putting into DataFrame)
nyc_unq = list(nyc_ab.unique())
nyc_unq.sort()
print nyc_unq
print len(nyc_unq)
# 133905
num = len(nyc_unq)
nyc_df = DataFrame(nyc_unq)
index = list(range(0,num))
print index
# Create dictionary map
dictionary = dict(zip(nyc_unq,index))
print dictionary
nyc_df[0].replace(dictionary,inplace=True)

# Create links
nyc_links = uws[['npi_a','npi_b','patient_cnt']]
nyc_links['npi_a'].replace(dictionary,inplace=True)
nyc_links['npi_b'].replace(dictionary,inplace=True)
links_col = ['source','target','value']
nyc_links.columns = links_col
nyc_links_json = nyc_links.to_json(orient='records')

# Write JSONs to files
with open('nodes.json','w') as f:
    f.write(nyc_nodes_json)

with open('links.json','w') as f:
    f.write(nyc_links_json)

# Create JSON file for D3 in shell
# cat head.txt nodes.json mid.txt links.json tail.txt > uws.json