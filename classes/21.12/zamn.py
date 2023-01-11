# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('data/moons.csv')
#df = pd.read_csv('circles.csv')
X0 = df.iloc[:, :-1].values
y = df.iloc[:, -1:].values

from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
ss.fit(X0)
X = ss.transform(X0)

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=2, init='k-means++')
y_pred = kmeans.fit_predict(X)
print(y_pred)

import matplotlib.pyplot as plt

plt.figure()
plt.scatter(df['x1'], df['x2'], c=y_pred, s=20, cmap='rainbow')
plt.title("Clusters")
plt.xlabel("x1")
plt.ylabel("x2")
plt.axis('equal')
plt.savefig('pic1.pdf')
plt.show()

"""
"""

from sklearn.cluster import AgglomerativeClustering

agg = AgglomerativeClustering(n_clusters=2)
y_pred = agg.fit_predict(X)
print(y_pred)

plt.figure()
plt.scatter(df['x1'], df['x2'], c=y_pred, s=20, cmap='rainbow')
plt.title("Clusters")
plt.xlabel("x1")
plt.ylabel("x2")
plt.axis('equal')
plt.savefig('pic2.pdf')
plt.show()

from scipy.cluster.hierarchy import dendrogram, ward

linkage_array = ward(X)
#dendrogram()

plt.figure(figsize=(20, 5))
dendrogram(linkage_array, truncate_mode='level', no_labels=True) #p=7
plt.title("Dendrogram")
plt.savefig('pic3.pdf')
plt.show()

"""
"""

from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.3, min_samples=10)
y_pred = dbscan.fit_predict(X) # noise: -1
print(y_pred)

plt.figure()
plt.scatter(df['x1'], df['x2'], c=y_pred, s=20, cmap='rainbow')
plt.title("Clusters")
plt.xlabel("x1")
plt.ylabel("x2")
plt.axis('equal')
plt.savefig('pic4.pdf')
plt.show()
