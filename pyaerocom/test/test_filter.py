#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:03:55 2019

@author: hannas
"""
import numpy as np
import pytest


from pyaerocom.filter import Filter
from pyaerocom.test.settings import TEST_RTOL, lustre_unavail

# Fixtures from other tests
from pyaerocom.io.test.test_read_aeronet_sunv3 import aeronetsunv3lev2_subset
from pyaerocom.test.test_griddeddata import data_tm5

def test_Filter_init():
    assert Filter('EUROPE').name == 'EUROPE-wMOUNTAINS'
    assert Filter('noMOUNTAINS-OCN-NAMERICA').name == 'NAMERICA-noMOUNTAINS-OCN'
    
def test_filter_attributes():
    f = Filter('WORLD-noMOUNTAINS-LAND')
    assert f.land_ocn == 'LAND'
    assert f.region_name == 'WORLD'
    assert f.name == 'WORLD-noMOUNTAINS-LAND'
    assert not f.region.is_htap
    

@lustre_unavail
def test_filter_griddeddata(data_tm5):
    
    model = data_tm5
    f1 = Filter('EUROPE-noMOUNTAINS-LAND') # europe only land
    f2 = Filter('EUROPE-noMOUNTAINS-OCN') # europe only ocean
    f3 = Filter('EUROPE') # europe total
    
    m_land = f1.apply(model)
    m_ocn  = f2.apply(model)
    m_all  = f3.apply(model)

    
    means = [np.nanmean(m_land.cube.data), np.nanmean(m_ocn.cube.data),
             np.nanmean(m_all.cube.data)]
    assert np.testing.assert_allclose(means, [0.16616775, 0.1314668, 0.13605888])

@lustre_unavail
def test_filter_ungriddeddata(aeronetsunv3lev2_subset):
    
    obs_data = aeronetsunv3lev2_subset
    
    f1 = Filter(name = 'NAMERICA-noMOUNTAINS')
    f2 = Filter(name = 'NAMERICA-noMOUNTAINS-OCN')
    f3 = Filter(name = 'NAMERICA-noMOUNTAINS-LAND')

    #gg = data.to_station_data_all()
    assert len(f1.apply(obs_data).unique_station_names) == 5
    assert len(f2.apply(obs_data).unique_station_names) == 29
    assert len(f3(obs_data).unique_station_names) == 3
    
@lustre_unavail
def test_filter_colocateddata():
    pass
# =============================================================================
#     data_coloc = pya.colocation.colocate_gridded_gridded(model, 
#                                                          sat, 
#                                                          ts_type='monthly', 
#                                                          filter_name='WORLD-noMOUNTAINS-OCN')
# 
#     assert data_coloc.data.sum().values - 111340.31777193633 < 0.001
# =============================================================================



if __name__ == '__main__':
    pytest.main(['test_filter.py'])