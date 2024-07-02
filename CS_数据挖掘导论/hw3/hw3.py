import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn import manifold
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

#read data
dfTrain = pd.read_csv("train_num.csv")
X_train = dfTrain.select_dtypes(include=[int, float])
X_train = X_train.apply(lambda x: x.fillna(x.mean()),axis=0)


#1.【1分】对作业2中的train_num.txt每一列的数值进行min-max的归一化处理，每个数值映射到[0,1]区间。
#------------------------------------------------------task1------------------------------------------------------
min_max_scaler = preprocessing.MinMaxScaler()
X_train_minmax = min_max_scaler.fit_transform(X_train)
print("min-max result: ", X_train_minmax)


# 2.【3分】对上述数据进行k-means聚类，取k=5。
#------------------------------------------------------task2------------------------------------------------------
kmeans = KMeans(n_clusters=5).fit(X_train_minmax)
print("k-means result: ", kmeans.labels_)


# 3.【4分】对上述数据进行DBSCAN聚类，通过调参生成5个聚类（NOISE点不计入这5个聚类中）。
#------------------------------------------------------task3------------------------------------------------------
dbscan = DBSCAN(eps = 0.6).fit(X_train_minmax)    #0.5～0.7之间都能生成5个类，选一个几类个数比较均衡的（？
print("dbscan result:", dbscan.labels_)


# 4.【2分】使用t-SNE对上述k-means和DBSCAN的聚类结果分别进行可视化。
#------------------------------------------------------task4------------------------------------------------------
tsne = manifold.TSNE(n_components= 2, init='pca', random_state=0)
fig = plt.figure(figsize=(8, 8))
Y = tsne.fit_transform(X_train_minmax)  # 转换后的输出
color = kmeans.labels_
colours = ListedColormap(['r','b','g','y','m'])
plt.scatter(Y[:, 0], Y[:, 1], c=color, cmap=colours)
plt.show()


tsne = manifold.TSNE(n_components= 2, init='pca', random_state=0)
fig = plt.figure(figsize=(8, 8))
Y = tsne.fit_transform(X_train_minmax)  # 转换后的输出
color = dbscan.labels_
colours = ListedColormap(['r','b','g','y','m'])
plt.scatter(Y[:, 0], Y[:, 1], c=color, cmap=colours)
plt.show()