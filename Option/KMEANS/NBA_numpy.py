import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

data = pd.read_csv("nba_2013.csv")
pg = data[data['pos'] == 'PG']
pg = pg[pg['g'] != 0]
pg = pg[pg['tov'] != 0]
pg['ppg'],pg['atr'] = pg['pts'] / pg['g'], pg['ast'] / pg['tov']

num_clusters=5
random_initial_points=np.random.choice(pg.index,size=num_clusters)
centroids = pg.loc[random_initial_points]
plt.scatter(pg['ppg'],pg['atr'],c='yellow')
plt.scatter(centroids['ppg'],centroids['atr'],c='red')
plt.title("Centroids")
plt.xlabel('Points Per Game',fontsize=13)
plt.ylabel('Assist Turnover Ratio',fontsize=13)

def centroids_to_dict(centroids):
    dictionary = dict()
    counter = 0
    for index,row in centroids.iterrows():
        coordinates = [row['ppg'],row['atr']]
        dictionary[counter]=coordinates
        counter += 1
    return dictionary

centroids_dict = centroids_to_dict(centroids)

def calculate_distance(centroid,player_values):
    root_distance=0

    for x in range(0,len(centroid)):
        difference = centroid[x]-player_values[x]
        squared_difference = difference**2
        root_distance += squared_difference

    euclid_distance = math.sqrt(root_distance)
    return euclid_distance
def assign_to_cluster(row):
    lowest_distance=-1
    closest_cluster=-1
    euclidean_distance=-1
    for cluster_id,centroid in centroids_dict.items():
        df_row = [row['ppg'],row['atr']]
        euclidean_distance = calculate_distance(centroid,df_row)
        if lowest_distance == -1:
            lowest_distance = euclidean_distance
            closest_cluster = cluster_id
        elif euclidean_distance < lowest_distance:
            lowest_distance = euclidean_distance
            closest_cluster = cluster_id
    return closest_cluster
pg['cluster'] = pg.apply(lambda row: assign_to_cluster(row), axis=1)
def visualize_clusters(df,num_clusters):
    colors = ['b','g','r','c','m','y','k']

    for n in range(num_clusters):
        clustered_df = df[df['cluster'] == n]
        plt.scatter(clustered_df['ppg'],clustered_df['atr'],c=colors[n-1])
        plt.xlabel('Points Per Game',fontsize=13)
        plt.ylabel('Assist Turnover Ratio',fontsize=13)

    plt.show()
visualize_clusters(pg, 5)
def recalculate_centroids(df):
    new_centroids_dict = dict()
    for cluster_id in range(0,num_clusters):
        class_all=df[df['cluster']==cluster_id]
        mean_ppg = class_all['ppg'].mean()
        mean_atr = class_all['atr'].mean()
        new_centroids_dict[cluster_id]= [mean_ppg,mean_atr]
    return new_centroids_dict

for i in range(10):
    centroids_dict = recalculate_centroids(pg)
    pg["cluster"] = pg.apply(lambda row:assign_to_cluster(row),axis=1)
    visualize_clusters(pg,5)

