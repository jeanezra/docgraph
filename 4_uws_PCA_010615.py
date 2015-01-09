import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print 0, datetime.datetime.now().isoformat()


# 1. Import dataset
uws_adj_mtrx = pd.read_table('uws_adj_mtrx_122214.txt',sep='\t',index_col=None,header=0)
print uws_adj_mtrx
print 1, datetime.datetime.now().isoformat()


# 2. Convert DataFrame to array
uws_arr = np.array(uws_adj_mtrx)
print uws_arr, len(uws_arr)
print 2, datetime.datetime.now().isoformat()
# 2 2015-01-07T12:58:54.521540


# 3. Fit PCA
pca = PCA(n_components=3)
uws_pca = pca.fit_transform(uws_arr)
print pca.explained_variance_ratio_
# array([ 0.38331514,  0.08696457,  0.04871541])
comp = pca.components_
print 3, datetime.datetime.now().isoformat()
# 3 2015-01-07T14:12:56.737124
uws_pca_df = pd.DataFrame(uws_pca)
uws_pca.to_csv('uws_3pca.txt',sep='\t',index=False,header=True)
comp_df = pd.DataFrame(comp)
comp_df.to_csv('uws_3pca_comp.txt',sep='\t',index=False,header=True)


# 4. Plot PCA
# http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#scatter-plots
uws2pca = pd.read_table('uws_2pca.txt',sep='\t',index_col=None,header=0)
x = np.array(uws2pca['0'])
y = np.array(uws2pca['1'])
plt.scatter(x,y)
plt.show()

uws3pca = pd.read_table('uws_3pca.txt',sep='\t',index_col=None,header=0)
x = np.array(uws3pca['0'])
y = np.array(uws3pca['1'])
z = np.array(uws3pca['2'])

comp = pd.read_table('uws_3pca_comp.txt',sep='\t',index_col=None,header=0)
V = np.array(comp)
pca_score = np.array([0.38331514,0.08696457,0.04871541])

fig = plt.figure()
plt.clf()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='r')
plt.show()


# 5. Find points of interest based on plot
x.max()
# 40643.218358071666
y.min()
# -20494.957743628409
uws2pca[uws2pca['0'] == 40643.218358071666]
# index = 569
# 1316968274
# Dr. Galina Mindlin
uws2pca[uws2pca['1'] == -20494.957743628409]
# index = 227
# 1275571408
# Dr. Daniel Sussman

uws2pca[uws2pca['1'] < -9494.957743628409]
# index = 20
# 1356574396
# Dr. Toai Huynh

x.max()
# 40643.218358071666
y.min()
# -20494.957743628409
z.min()
# -7826.9680902395912

uws3pca[uws3pca['0'] == 40643.218358071666]
# index: 569
uws3pca[uws3pca['1'] == -20494.957743628409]
# index: 227
uws3pca[uws3pca['2'] == -7826.9680902395912]
# index: 191
# 1790818144
# Dr. Stephan Lansey