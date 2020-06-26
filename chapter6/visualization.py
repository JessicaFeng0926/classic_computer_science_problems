from typing import List
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from kmeans import KMeans

def visualization(clusters: List[KMeans.Cluster], 
                  x_label: str, y_label: str) -> None:
    '''只能做二维的可视化'''
    clusters_dict = {x_label:[],y_label:[],'cluster':[]}
    for index,cluster in enumerate(clusters):
        for point in cluster.points:
            clusters_dict[x_label].append(point.dimensions[0])
            clusters_dict[y_label].append(point.dimensions[1])
            clusters_dict['cluster'].append(index)
            
    df = pd.DataFrame.from_dict(clusters_dict)
    fig = sns.lmplot(x=x_label,
                     y=y_label,
                     data=df,
                     hue='cluster',
                     fit_reg=False)
   
    plt.show()
    
    

    





