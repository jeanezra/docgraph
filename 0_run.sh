# 0. Generate state subset
#'1 Docgraph + NPPES 102814.py'

### UPPER WEST SIDE
# 1. Generate neighborhood dataset using merged in
1a_generate_subset.py nyc.txt uws.txt 'uws_zip()'

# 2. Create edge weight list
cut -d$'\t' -f 1-3 uws.txt > uws_weighted_edgelist.txt
scp white:~/docgraph/uws_weighted_edgelist.txt .
cat uws_weighted_edgelist.txt | sed "1 d" > uws_weighted_edgelist_nohead.txt

# 3. Create adjacency matrix using edge weight list
python 6_networkx.py uws_weighted_edgelist_nohead.txt uws_adj_mtrx_111915.txt
#Time elapsed: 0:00:23.562098

# 4. Calculate basic social network analysis metrics
python 6a_networkx_stats.py uws_weighted_edgelist_nohead.txt uws_sna_metrics_111915.txt
#Time elapsed: 0:00:55.111452

# 5. Calculate weight stats
python 2b_weight_chunk.py uws_adj_mtrx_111915.txt uws_weight_stats_111915.txt
#Time elapsed: 0:00:47.898116

# 6. Paste datasets together
wc -l ../uws_adj_mtrx_111915.txt
#8581
wc -l ../uws_sna_metrics_111915.txt
#8581
wc -l ../uws_weight_stats_111915.txt
#8581

cat ../uws_adj_mtrx_111915.txt | awk '{print NF}' FS='\t' | head -2
#8580
cat ../uws_sna_metrics_111915.txt | awk '{print NF}' FS='\t' | head -2
#6
cat ../uws_weight_stats_111915.txt | awk '{print NF}' FS='\t' | head -2
#7

paste -d$'\t' ../uws_adj_mtrx_111915.txt ../uws_sna_metrics_111915.txt ../uws_weight_stats_111915.txt > ../uws_mtx_sna_weights_111915.txt
wc -l ../uws_mtx_sna_weights_111915.txt
#8581
cat ../uws_mtx_sna_weights_111915.txt | awk '{print NF}' FS='\t' | head -2
#8593

## Annotations - for revise weight stats features
#cut -d$'\t' -f 1 uws_sna_metrics_111915.txt > uws_source_key.txt
#paste -d$'\t' uws_source_key.txt uws_weight_stats_111915.txt > uws_key_weight_stats_111915.txt

# 7. Extract and transform healthcare data (e.g. specialty, sole proprietor, organization subpart)
python 3a_healthcare_data.py uws.txt uws_sna_metrics_111915.txt uws_healthcare.txt

wc -l ../uws_healthcare.txt
#35470
cat ../uws_mtx_sna_weights_111915.txt | awk '{print NF}' FS='\t' | head -2

paste -d$'\t' ../uws_mtx_sna_weights_111915.txt ../uws_healthcare.txt > ../uws_mtx_sna_weights_healthcare_111915.txt
wc -l ../uws_mtx_sna_weights_healthcare_111915.txt
cat ../uws_mtx_sna_weights_healthcare_111915.txt | awk '{print NF}' FS='\t' | head -2





### UPPER EAST SIDE
# 1. Generate neighborhood dataset using merged in
1a_generate_subset.py nyc.txt ues.txt 'ues_zip()'

# 2. Create edge weight list
cut -d$'\t' -f 1-3 ues.txt > ues_weighted_edgelist.txt
scp white:~/docgraph/ues_weighted_edgelist.txt .
cat ues_weighted_edgelist.txt | sed "1 d" > ues_weighted_edgelist_nohead.txt

# 3. Create adjacency matrix using edge weight list
python 6_networkx.py ues_weighted_edgelist_nohead.txt ues_adj_mtrx_121015.txt
#Time elapsed: 0:30:55.335107

# 4. Calculate basic social network analysis metrics
python 6a_networkx_stats.py ues_weighted_edgelist_nohead.txt ues_sna_metrics_121015.txt
#Time elapsed: 1:04:36.889905

# 5. Calculate weight stats
python 2b_weight_chunk.py ues_adj_mtrx_121015.txt ues_weight_stats_121015.txt
#Time elapsed: 0:20:50.496167

# 6. Paste datasets together
wc -l ../ues_adj_mtrx_121015.txt
#8581
wc -l ../ues_sna_metrics_121015.txt
#8581
wc -l ../ues_weight_stats_121015.txt
#8581

cat ../ues_adj_mtrx_121015.txt | awk '{print NF}' FS='\t' | head -2
#8580
cat ../ues_sna_metrics_121015.txt | awk '{print NF}' FS='\t' | head -2
#6
cat ../ues_weight_stats_121015.txt | awk '{print NF}' FS='\t' | head -2
#7

paste -d$'\t' ../ues_adj_mtrx_121015.txt ../ues_sna_metrics_121015.txt ../ues_weight_stats_121015.txt > ../ues_mtx_sna_weights_121015.txt
wc -l ../ues_mtx_sna_weights_121015.txt
#8581
cat ../ues_mtx_sna_weights_121015.txt | awk '{print NF}' FS='\t' | head -2
#8593

## Annotations - for revise weight stats features
#cut -d$'\t' -f 1 ues_sna_metrics_121015.txt > ues_source_key.txt
#paste -d$'\t' ues_source_key.txt ues_weight_stats_121015.txt > ues_key_weight_stats_121015.txt

# 7. Extract and transform healthcare data (e.g. specialty, sole proprietor, organization subpart)
python 3a_healthcare_data.py ues.txt ues_sna_metrics_121015.txt ues_healthcare.txt
# Time elapsed: 0:00:32.526777

wc -l ../ues_healthcare.txt
#35470
cat ../ues_mtx_sna_weights_121015.txt | awk '{print NF}' FS='\t' | head -2

paste -d$'\t' ../ues_mtx_sna_weights_121015.txt ../ues_healthcare.txt > ../ues_mtx_sna_weights_healthcare_121015.txt
wc -l ../ues_mtx_sna_weights_healthcare_121015.txt
cat ../ues_mtx_sna_weights_healthcare_121015.txt | awk '{print NF}' FS='\t' | head -2





### WASHINGTON HEIGHTS
# 1. Generate neighborhood dataset using merged in
1a_generate_subset.py nyc.txt wash_hgts.txt 'wash_hgts_zip()'

# 2. Create edge weight list
cut -d$'\t' -f 1-3 wash_hgts.txt > wash_hgts_weighted_edgelist.txt
scp white:~/docgraph/wash_hgts_weighted_edgelist.txt .
cat wash_hgts_weighted_edgelist.txt | sed "1 d" > wash_hgts_weighted_edgelist_nohead.txt

# 3. Create adjacency matrix using edge weight list
python 6_networkx.py wash_hgts_weighted_edgelist_nohead.txt wash_hgts_adj_mtrx_121415.txt
#Time elapsed: 0:30:55.335107

# 4. Calculate basic social network analysis metrics
python 6a_networkx_stats.py wash_hgts_weighted_edgelist_nohead.txt wash_hgts_sna_metrics_121415.txt
#Time elapsed: 0:05:49.727062

# 5. Calculate weight stats
python 2b_weight_chunk.py wash_hgts_adj_mtrx_121415.txt wash_hgts_weight_stats_121415.txt
#Time elapsed: 0:06:33.074442

# 6. Paste datasets together
wc -l ../wash_hgts_adj_mtrx_121415.txt
#22874
wc -l ../wash_hgts_sna_metrics_121415.txt
#22874
wc -l ../wash_hgts_weight_stats_121415.txt
#22874

cat ../wash_hgts_adj_mtrx_121415.txt | awk '{print NF}' FS='\t' | head -2
#8580
cat ../wash_hgts_sna_metrics_121415.txt | awk '{print NF}' FS='\t' | head -2
#6
cat ../wash_hgts_weight_stats_121415.txt | awk '{print NF}' FS='\t' | head -2
#7

paste -d$'\t' ../wash_hgts_adj_mtrx_121415.txt ../wash_hgts_sna_metrics_121415.txt ../wash_hgts_weight_stats_121415.txt > ../wash_hgts_mtx_sna_weights_121415.txt
wc -l ../wash_hgts_mtx_sna_weights_121415.txt
#22891
cat ../wash_hgts_mtx_sna_weights_121415.txt | awk '{print NF}' FS='\t' | head -2
#22891

## Annotations - for revise weight stats features
#cut -d$'\t' -f 1 wash_hgts_sna_metrics_121415.txt > wash_hgts_source_key.txt
#paste -d$'\t' wash_hgts_source_key.txt wash_hgts_weight_stats_121415.txt > wash_hgts_key_weight_stats_121415.txt

# 7. Extract and transform healthcare data (e.g. specialty, sole proprietor, organization subpart)
python 3a_healthcare_data.py wash_hgts.txt wash_hgts_sna_metrics_121415.txt wash_hgts_healthcare.txt
#Time elapsed: 0:00:30.272996

wc -l ../wash_hgts_healthcare.txt
#22874
cat ../wash_hgts_mtx_sna_weights_121415.txt | awk '{print NF}' FS='\t' | head -2
#22891
paste -d$'\t' ../wash_hgts_mtx_sna_weights_121415.txt ../wash_hgts_healthcare.txt > ../wash_hgts_mtx_sna_weights_healthcare_121415.txt
wc -l ../wash_hgts_mtx_sna_weights_healthcare_121415.txt
#22874
cat ../wash_hgts_mtx_sna_weights_healthcare_121415.txt | awk '{print NF}' FS='\t' | head -2
#23018