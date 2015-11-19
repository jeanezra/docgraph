As part of the Freedom of Information Act (FOIA), Fred Trotter requested physician "referral" data. This repo uses the within 30-day "referral" data from Medicare in 2012.

The goal is to merge the dataset with the National Plan & Provider Enumeration System (NPPES) dataset, as well as other useful open health data resources for a social network analysis. 

A JSON file is created to visualize the data in D3; a delimited file is created to do analysis in Gephi, an open source social network analysis software; and an adjacency matrix is created to perform more sophisticated analysis using machine learning algorithms.



1. Generate subset of interest
1_generate_subset.py

2. Construct adjacency matrix for 1.
2_adjacency_matrix.py

3. Compute social network metrics & other domain-specific variables (e.g. specialty, provider type)
