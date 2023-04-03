# %%

import pandas as pd
from src_pp.path_pp import PPPaths

# %%

# a cluster consists of multiple households
# for each household we do have a per capita consumption value
# however, households are of varying size. Hence, simply averaging all per capita
# consumption values would induce a weighting 
# eventually we want to get average per capita consumption per cluster

def load_data_nigeria():
    
    # load socio-economic household data
    fname = PPPaths.raw_data_path / "cons_agg_wave3_visit1.csv"
    raw_consumption_data = pd.read_csv(fname)
    raw_consumption_data = raw_consumption_data.loc[:, ['hhid', 'hhsize', 'totcons']]

    # load geo data
    fname = PPPaths.raw_data_path / "nga_householdgeovars_y3.csv"
    raw_geo_data = pd.read_csv(fname)
    raw_geo_data = raw_geo_data.loc[:, ['hhid', 'LAT_DD_MOD', 'LON_DD_MOD']]
    raw_geo_data.rename(columns={'LAT_DD_MOD': 'cluster_lat', 
                                'LON_DD_MOD': 'cluster_lon'}, inplace=True)

    # merge data
    full_data = raw_consumption_data.merge(raw_geo_data, on='hhid', how='outer')

    # compute aggregate consumption per household, totcons is per capita

    full_data['cons_ph'] = full_data['totcons'] * full_data['hhsize']
    full_data = full_data.drop(columns=['totcons'])

    do_ppp_adjust = False
    if do_ppp_adjust is True:
        raise ValueError('Purchasing power adjustment not correctly implemented yet')
        # purchasing power parity for nigeria in 2015 (https://data.worldbank.org/indicator/PA.NUS.PRVT.PP?locations=NG)
        ppp = 95.255

        # adjust for purchasing power parity
        full_data['cons_ph'] = full_data['cons_ph'] / ppp / 365

    # drop NAs
    # some hhids have geodata but no data for household size and consumption
    # xx_inds_na = full_data.isna().any(axis=1)
    # full_data.loc[xx_inds_na, :]

    clean_data = full_data.dropna().copy()
    clean_data['country'] = 'nigeria'
    
    return clean_data


def compute_cluster_avg_consumption_per_capita(clean_data):
    # aggregate people and consumption per cluster
    cluster_data = clean_data.drop(columns=['hhid']).copy()
    cluster_data = cluster_data.groupby(['cluster_lat', 'cluster_lon', 'country']).sum().reset_index()
    
    # compute average per capita consumption
    cluster_data['cons_pc'] = cluster_data['cons_ph'] / cluster_data['hhsize']
    
    return cluster_data

# %%

if __file__ == '__main__':
    
    # %%
    clean_data = load_data_nigeria()
    cluster_data = compute_cluster_avg_consumption_per_capita(clean_data)
    
    fname = PPPaths.processed_data_path / "cluster_data.csv"
    cluster_data.reset_index().to_csv(fname, index=False)
    
    