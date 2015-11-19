### UPPER WEST SIDE

# Generate neighborhood dataset using merged in
1a_generate_subset.py nyc.txt uws.txt 'uws_zip()'

# Create edge weight list
cut -d$'\t' -f 1-3 uws.txt > uws_weighted_edgelist.txt
scp white:~/docgraph/uws_weighted_edgelist.txt .
cat uws_weighted_edgelist.txt | sed "1 d" > uws_weighted_edgelist_nohead.txt

# Create adjacency matrix using edge weight list
python 6_networkx.py uws_weighted_edgelist_nohead.txt uws_adj_mtrx_111915.txt
#Time elapsed: 0:00:23.562098

# Calculate basic social network analysis metrics
python 6a_networkx_stats.py uws_weighted_edgelist_nohead.txt uws_sna_metrics_111915.txt
#Time elapsed: 0:00:55.111452

# Calculate weight stats
python 2b_weight_chunk.py uws_adj_mtrx_111915.txt uws_weight_stats_111915.txt
#Time elapsed: 0:00:47.898116

# Paste datasets together
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

# Extract and transform healthcare data (e.g. specialty, provider type)
