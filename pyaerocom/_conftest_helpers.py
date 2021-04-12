#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:57:09 2020

@author: jonasg
"""
from pyaerocom import StationData, ColocatedData, Filter
import numpy as np
import pandas as pd
import xarray as xr


def _load_coldata_tm5_aeronet_from_scratch(file_path):
    from xarray import open_dataarray
    from pyaerocom import ColocatedData
    arr = open_dataarray(file_path)
    if '_min_num_obs' in arr.attrs:
        info = {}
        for val in arr.attrs['_min_num_obs'].split(';')[:-1]:
            to, fr, num = val.split(',')
            if not to in info:
                info[to] = {}
            if not fr in info[to]:
                info[to][fr] = {}
            info[to][fr] = int(num)
        arr.attrs['min_num_obs'] = info
    cd = ColocatedData()
    cd.data = arr
    return cd

def create_fake_station_data(addvars, varinfo, varvals, start, stop, freq,
                              meta):
    if isinstance(addvars, str):
        addvars = [addvars]
    stat = StationData()
    stat.update(**meta)
    dtime = pd.date_range(start, stop, freq=freq).values
    stat['dtime'] = dtime
    for var in addvars:
        if var in varinfo:
            stat.var_info[var] = varinfo[var]
        if isinstance(varvals, dict):
            val = varvals[var]
        else:
            val = varvals
        stat[var] = np.ones(len(dtime)) * val
    return stat

def create_fake_stationdata_list():
    stats = [
        create_fake_station_data('concpm10', {'concpm10': {'units' : 'ug m-3'}},
                                  10, '2010-01-01', '2010-12-31', 'd',
                                  {'awesomeness' : 10,
                                   'data_revision' : 20120101,
                                   'ts_type' : 'daily', 'latitude' : 10,
                                   'longitude' : 20, 'altitude' : 0,
                                   'station_name' : 'FakeSite'}),
        # overlaps with first one
        create_fake_station_data('concpm10', {'concpm10': {'units' : 'ug m-3'}},
                                  20, '2010-06-01', '2011-12-31', 'd',
                                  {'awesomeness' : 12,
                                   'data_revision' : 20110101,
                                   'ts_type' : 'daily', 'latitude' : 42.001,
                                   'longitude' : 20, 'altitude' : 0.1,
                                   'station_name' : 'FakeSite'}),

        # monthly, but missing ts_type and wrong unit
        create_fake_station_data('concpm10', {'concpm10': {'units' : 'mole mole-1'}},
                                  20, '2014-01-01', '2015-12-31', '3MS',
                                  {'awesomeness' : 2,
                                   'data_revision' : 20140101,
                                   'latitude' : 42.001,
                                   'longitude' : 20, 'altitude' : 0.1,
                                   'station_name' : 'FakeSite'}),

        # invalid ts_type
        create_fake_station_data('concpm10', {'concpm10': {'units' : 'ug m-3'}},
                                  20, '1850', '2020', '1000d',
                                  {'awesomeness' : 15,
                                   'data_revision' : 20130101,
                                   'ts_type' : '1000daily', 'latitude' : 42.001,
                                   'longitude' : 20, 'altitude' : 0.1,
                                   'station_name' : 'FakeSite'}),

        # new variable and monthly
        create_fake_station_data('od550aer', {'od550aer': {'units' : '1'}},
                                  1, '2005', '2012', 'MS',
                                  {'awesomeness' : 42,
                                   'data_revision' : 20200101,
                                   'ts_type' : 'monthly', 'latitude' : 42.001,
                                   'longitude' : 20, 'altitude' : 0.1,
                                   'station_name' : 'FakeSite'}),

        create_fake_station_data('od550aer', {'od550aer': {'units' : '1'}},
                                  0.1, '2008', '2009', '60d',
                                  {'awesomeness' : 46,
                                   'data_revision' : 20200101,
                                   'ts_type' : '60daily', 'latitude' : 22.001,
                                   'longitude' : 10, 'altitude' : 100,
                                   'station_name' : 'FakeSite2'})
        ]

    stat_werr = create_fake_station_data('od550aer', {'od550aer': {'units' : '1'}},
                                  0.2, '2010', '2016', '10d',
                                  {'awesomeness' : 30,
                                   'data_revision' : 20200101,
                                   'ts_type' : '10daily', 'latitude' : 22.001,
                                   'longitude' : 10, 'altitude' : 100,
                                   'station_name' : 'FakeSite2'})
    stat_werr.data_err['od550aer'] = np.ones(len(stat_werr.dtime))*9999
    stats.append(stat_werr)
    return stats

def _create_fake_coldata_3d():
    var = 'concpm10'
    filter_name = 'WORLD-wMOUNTAINS'
    regfilter = Filter(name=filter_name)

    dtime = pd.date_range('2000-01-01', '2019-12-31', freq='MS') + np.timedelta64(14, 'D')

    lats = [-80, 0, 70, 0.1]
    lons = [-150, 0, 100, 0.1]
    alts = [0, 100, 2000, 10]

    timenum = len(dtime)
    statnum = len(lats)
    c = 1
    statnames = []
    for lat in lats:
        statnames.append(f'FakeStation{c}')
        c+=1
    data = np.ones((2, timenum, statnum))
    xrange_modulation = np.linspace(0,np.pi*40,240)
    data[1] += 0.1 #+10% model bias

    # 1. SITE: modify first site (sin , cos waves)
    data[0,:,0] += np.sin(xrange_modulation)
    data[1,:,0] += np.cos(xrange_modulation) # phase shifted to obs

    years = dtime.year.values
    # 2. SITE: modify second site (yearly stepwise increase, double as
    # pronounced in obs than in model)
    c = 0
    for year in np.unique(years):
        mask = years == year
        data[0,mask,1] += c*0.4
        data[1,mask,1] += c*0.2
        c+=1

    # 3 SITE: add noise to model and obs
    data[0,:,2] += np.random.rand(timenum)
    data[1,:,2] += np.random.rand(timenum)

    meta = {
            'data_source'       :   ['fakeobs',
                                     'fakemod'],
            'var_name'          :   [var,var],
            'ts_type'           :   'monthly', # will be updated below if resampling
            'filter_name'       :   filter_name,
            'ts_type_src'       :   ['monthly', 'daily'],
            'start_str'         :   dtime[0].strftime('%Y%m%d'),
            'stop_str'          :   dtime[-1].strftime('%Y%m%d'),
            'var_units'         :   ['ug m-3','ug m-3'],
            'vert_scheme'       :   'surface',
            'data_level'        :   3,
            'revision_ref'      :   '20210409',
            'from_files'        :   [],
            'from_files_ref'    :   None,
            'stations_ignored'  :   None,
            'colocate_time'     :   False,
            'obs_is_clim'       :   False,
            'pyaerocom'         :   '0.11.0',
            'apply_constraints' :   True,
            'min_num_obs'       :   3,
            'resample_how'      :   None}


    meta.update(regfilter.to_dict())


    # create coordinates of DataArray
    coords = {'data_source' : meta['data_source'],
              'time'        : dtime,
              'station_name': statnames,
              'latitude'    : ('station_name', lats),
              'longitude'   : ('station_name', lons),
              'altitude'    : ('station_name', alts)
              }

    dims = ['data_source', 'time', 'station_name']
    cd = ColocatedData(data=data, coords=coords, dims=dims, name=var,
                         attrs=meta)

    return cd

def _create_fake_coldata_4d():
    _lats_fake = np.arange(30,70,10)
    _lons_fake = np.arange(0,40,10)
    _time_fake = pd.date_range('2010-01', '2010-03', freq='MS')
    _data_fake = np.ones((2, len(_time_fake), len(_lats_fake), len(_lons_fake)))

    coords = {'data_source' : ['obs', 'mod'],
              'time'        : _time_fake,
              'latitude'    : _lats_fake,
              'longitude'   : _lons_fake
              }

    dims = ['data_source', 'time', 'latitude', 'longitude']
    # set all NaN in one obs coordinate
    _data_fake[0,:,0,0] = np.nan
    return ColocatedData(data=_data_fake, coords=coords, dims=dims)

def _create_fake_coldata_5d():
    _lats_fake = [10,20]
    _lons_fake = [42,43]
    _time_fake = pd.date_range('2010-01', '2010-03', freq='MS')
    _wvl_fake = [100,200,300]
    _data_fake = np.ones((2, len(_time_fake), len(_lats_fake), len(_lons_fake), len(_wvl_fake)))

    coords = {'data_source' : ['fakeobs', 'fakemod'],
              'time'        : _time_fake,
              'latitude'    : _lats_fake,
              'longitude'   : _lons_fake,
              'wvl'         : _wvl_fake
              }

    dims = ['data_source', 'time', 'latitude', 'longitude','wvl']
    # set all NaN in one obs coordinate
    arr = xr.DataArray(data=_data_fake, coords=coords, dims=dims)
    cd = ColocatedData(np.ones((2,2,2)))
    cd.data = arr
    return cd

if __name__ == '__main__':
    import pyaerocom as pya
    import matplotlib.pyplot as plt
    plt.close('all')
    cd = _create_fake_coldata_3d()
    cd = _create_fake_coldata_4d()
    cd5 = _create_fake_coldata_5d()

    stats = cd.calc_statistics()
    print('Normal stats')
    print(stats)

    arr = cd.data

    # ONE WAY: flatten certain dimensions and compute stats from that
    avg_alltimes = np.nanmean(arr.data, axis=1)
    obs, mod = avg_alltimes[0], avg_alltimes[1]

    stats_spatial = pya.mathutils.calc_statistics(mod, obs)
    print('Spatial stats')
    print(stats_spatial)

    avg_allsites = np.nanmean(arr.data, axis=2)
    obs, mod = avg_allsites[0], avg_allsites[1]

    stats_temporal = pya.mathutils.calc_statistics(mod, obs)
    print('Temporal stats')
    print(stats_temporal)

    # OTHER WAY: calculate corr for each entry in one dimension (e.g. corr for
    # each site or corr for january from all sites) and then
    corr_time = xr.corr(arr[1],arr[0], dim='time')
    corr_stats = xr.corr(arr[1],arr[0], dim='station_name')

    cd.plot_scatter()



