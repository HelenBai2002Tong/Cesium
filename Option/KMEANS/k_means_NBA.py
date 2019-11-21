import pandas
import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.cluster import KMeans
data = pandas.read_csv("nba_2013.csv")
pg = data[data['pos'] == 'PG']
pg = pg[pg['g'] != 0]
pg = pg[pg['tov'] != 0]
pg['ppg'],pg['atr'] = pg['pts'] / pg['g'], pg['ast'] / pg['tov'] 

cluster_num = 5

def visualize_clusters(pg,cluster_num):
    colors = ['b','g','r','c','m','y','k']

    for n in range(cluster_num):
        clustered_pg = pg[pg['cluster'] == n]
        plt.scatter(clustered_pg['ppg'],clustered_pg['atr'],c=colors[n-1])
        plt.xlabel('Points Per Game',fontsize=13)
        plt.ylabel('Assist Turnover Ratio',fontsize=13)
    
    plt.show()

kmeans = KMeans(n_clusters=cluster_num)
kmeans.fit(pg[['ppg', 'atr']])
pg['cluster'] = kmeans.labels_

visualize_clusters(pg, cluster_num)

'''
initial_point = np.random.choice(pg.index,size = cluster_num)
cluster = pg.loc[initial_point]






def cluster_to_dict(cluster):
    dictionary = dict()
    counter = 0
    for index,row in cluster.iterrows():
        coordinates = [row['ppg'],row['atr']]
        dictionary[counter]=coordinates
        counter += 1
    return dictionary 

def calculate_distance(cluster,player_values):
    root_distance=0

    for x in range(0,len(cluster)):
        difference = cluster[x]-player_values[x]
        squared_difference = difference**2
        root_distance += squared_difference

    euclid_distance = math.sqrt(root_distance)
    return euclid_distance

def assign_to_cluster(row):
    lowest_distance=-1
    closest_cluster=-1
    euclidean_distance=-1

    for cluster_id,cluster in cluster_dict.items():
        df_row = [row['ppg'],row['atr']]
        euclidean_distance = calculate_distance(cluster,df_row)
        if lowest_distance == -1:
            lowest_distance = euclidean_distance
            closest_cluster = cluster_id
        elif euclidean_distance < lowest_distance:
            lowest_distance = euclidean_distance
            closest_cluster = cluster_id
    return closest_cluster

def recalculate_cluster(df):
    new_cluster_dict = dict()
    #0..1..2..3..4
    for cluster_id in range(0,num_clusters):
        class_all=df[df['cluster']==cluster_id]
        mean_ppg = class_all['ppg'].mean()
        mean_atr = class_all['atr'].mean()
        new_centroids_dict[cluster_id]= [mean_ppg,mean_atr]
    return new_centroids_dict


'''