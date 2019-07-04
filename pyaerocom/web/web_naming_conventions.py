#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:31:56 2019

@author: jonasg
"""

VAR_MAPPING = {'od550aer'       : ['AOD', '2D', 'Optical properties'],
               'od550lt1aer'    : ['AOD<1um', '2D', 'Optical properties'],
               'od550gt1aer'    : ['AOD>1um', '2D', 'Optical properties'],
               'abs550aer'      : ['AAOD', '2D', 'Optical properties'],
               'ang4487aer'     : ['AE', '2D', 'Optical properties'],
               'scatc550dryaer' : ['Scat. coef. (dry)', '3D', 'Optical properties'],
               'scatc550aer'    : ['Scat. coef.', '3D', 'Optical properties'],
               'absc550aer'     : ['Abs. coef.', '3D', 'Optical properties'],
               'ec532aer'       : ['Ext. coeff.', '3D', 'Optical properties'],
               'bscatc532aer'   : ['Backscat. coeff.', '3D', 'Optical properties'],
               'sconcpm10'      : ['PM10', '3D', 'Particle concentrations'],
               'sconcpm25'      : ['PM2.5', '3D', 'Particle concentrations'],
               'sconcso4'       : ['SO4 (Aerosol)', '3D', 'Particle concentrations'],
               'sconcso4pr'     : ['SO4 (precip.)', '3D', 'Particle concentrations'],
               'sconco3'        : ['O3', '3D', 'Gas concentrations'],
               'sconcso2'       : ['SO2', '3D', 'Gas concentrations'],
               }