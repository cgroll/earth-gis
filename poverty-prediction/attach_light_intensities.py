# %%
import pandas as pd
import numpy as np
import geoio
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

from src_pp.utils import create_lat_lon_square
from src_pp.path_pp import PPPaths


# %%
if __file__ == '__main__':
    
    # %%
    
    fname = PPPaths.processed_data_path / "cluster_data.csv"
    cluster_data = pd.read_csv(fname, index_col='index')

    # %% load nightlight data
    fname = PPPaths.raw_data_path / "viirs_2015_75N060W.tif"
    tiffile = geoio.GeoImage(str(fname))
    
    tif_array = np.squeeze(tiffile.get_data())

    # %%
    
    cluster_nightlights = []
    for i,r in tqdm(cluster_data.iterrows(), total=cluster_data.shape[0]):
        min_lat, min_lon, max_lat, max_lon = create_lat_lon_square(10, r.cluster_lat, r.cluster_lon)
        
        xminPixel, ymaxPixel = tiffile.proj_to_raster(min_lon, min_lat)
        xmaxPixel, yminPixel = tiffile.proj_to_raster(max_lon, max_lat)
        assert xminPixel < xmaxPixel, print(r.cluster_lat, r.cluster_lon)
        assert yminPixel < ymaxPixel, print(r.cluster_lat, r.cluster_lon)
        if xminPixel < 0 or xmaxPixel >= tif_array.shape[1]:
            print(f"no match for {r.cluster_lat}, {r.cluster_lon}")
            raise ValueError()
        elif yminPixel < 0 or ymaxPixel >= tif_array.shape[0]:
            print(f"no match for {r.cluster_lat}, {r.cluster_lon}")
            raise ValueError()
        xminPixel, yminPixel, xmaxPixel, ymaxPixel = int(xminPixel), int(yminPixel), int(xmaxPixel), int(ymaxPixel)
        cluster_nightlights.append(tif_array[yminPixel:ymaxPixel,xminPixel:xmaxPixel].mean())
        
    # %% 
    
    cluster_data['nightlights'] = cluster_nightlights
    
    # %%
    
    cluster_data.head(3)
    
    # %%
    
    # Usual boxplot
    ax = sns.boxplot(x='country', y='nightlights', data=cluster_data)
    
    # Add jitter with the swarmplot function
    ax = sns.swarmplot(x='country', y='nightlights', data=cluster_data, color="grey")
    plt.show()
    #cluster_data['nightlights'].quantile(0.99)
    
    # %% 
    cluster_data['nightlights'].mean()
    
    # %%
    
    