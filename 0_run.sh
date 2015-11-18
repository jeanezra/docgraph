# Generate neighborhood dataset using merged in
1a_generate_subset.py nyc.txt uws.txt 'uws_zip()'

# Create edge weight list
cut -d$'\t' -f 1-3 uws.txt > uws_weighted_edgelist.txt
scp white:~/docgraph/uws_weighted_edgelist.txt .
cat uws_weighted_edgelist.txt | sed "1 d" > uws_weighted_edgelist_nohead.txt

# Create adjacency matrix using edge weight list
6_networkx.py uws_weighted_edgelist_nohead.txt uws_adj_mtrx_111815.txt

# Calculate basic social network analysis metrics
6a_networkx_stats.py uws_weighted_edgelist_nohead.txt uws_sna_metrics_111815.txt

# Calculate weight stats
python 2b_weight_chunk.py uws_adj_mtrx_111815.txt uws_weight_stats_111815.txt