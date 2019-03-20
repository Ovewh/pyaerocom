#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 09:17:17 2019

@author: paulinast
"""


import numpy as np
from collections import OrderedDict as od
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom import const, print_log

from pyaerocom.stationdata import StationData
import pandas as pd


# from os import glob


class ReadGAW(ReadUngriddedBase):
    
    
    """Interface for reading DMS data

    .. seealso::
        
        Base classes :class:`ReadAeronetBase` and :class:`ReadUngriddedBase`

    """
    #: Mask for identifying datafiles 
    _FILEMASK = '*.dat'
    
    #: version log of this class (for caching)
    __version__ = '0.01'  # ???
    
    #: Name of dataset (OBS_ID)
    DATA_ID = const.DMS_AMS_CVO_NAME
    
    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]
    
    #: dictionary assigning temporal resolution flags for supported datasets
    #: that are provided in a defined temporal resolution
    TS_TYPE = 'daily'
    
    #: default variables for read method
    DEFAULT_VARS = ['vmrdms']
    
    #: value corresponding to invalid measurement
    NAN_VAL = -999999999999.99
    
    #: dictionary specifying the file column names (values) for each Aerocom 
    #: variable (keys)
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE['vmrdms'] = 'dimethylsulfide'
    VAR_NAMES_FILE['vmrdms_nd'] = 'ND'
    VAR_NAMES_FILE['vmrdms_flag'] = 'F'

    #: List of variables that are provided by this dataset (will be extended 
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE.keys())

    INSTRUMENT_NAME = 'unknown'

    
    #def get_file_list(self):
     #   all_files = glob.glob(self.DATASET_PATH)
      #  return all_files
    
# =============================================================================
#     DATASET_PATH = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/PYAEROCOM/DMS_AMS_CVO/data/'
#     DATASET_NAME = 'DMS_AMS_CVO'
# =============================================================================
    
    @property
    def DATASET_NAME(self): 
        return self.DATA_ID
    
    def read_file(self, filename, vars_to_retrieve=None, 
                  vars_as_series=False):
        """Read DMS file 
        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read. If None, use
            :attr:`DEFAULT_VARS`
        vars_as_series : bool
            if True, the data columns of all variables in the result dictionary
            are converted into pandas Series objects
            
        Returns
        -------
        StationData
            dict-like object containing results
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        
        
        # implemented in base class
        # comment this because we don't need to compute any variables
        #vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
       
        #create empty data object (a dictionary with extended functionality)
        data_out = StationData()
        data_out.data_id = self.DATA_ID
        data_out.dataset_name = self.DATASET_NAME
        
        # Commented because I don't define META_NAMES_FILE
        # create empty arrays for meta information+
        #for item in self.META_NAMES_FILE:
        #    data_out[item] = []
            
        # create empty arrays for all variables that are supposed to be read
        # from file
        #for var in vars_to_read:
         #   data_out[var] = []
         
         
        
        # Iterate over the lines of the file
        self.logger.info("Reading file {}".format(filename))
        
        
        #with open(path2dir+'ams137s00.lsce.as.fl.dimethylsulfide.nl.da.dat', 'r') as f: 
        with open(filename, 'r') as f:         
            
            # metadata (first rows in the file)
            meta = [next(f).split(':', 1)[1] for x in range(26)]

            f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            
            x = []  # data
            for line in f:
                columns = line.split()
                x.append(columns)
        
         
        # Select the metadata that I want and reformat
        # and replace whitespaces in strings with underscore  
        #data_out = {}
        
        data_out['station_name'] = meta[6].strip().replace(' ', '_')
        data_out['longitude'] = float(meta[12].strip())
        data_out['latitude'] = float(meta[11].strip())
        data_out['altitude'] = float(meta[13].strip())
        data_out['filename'] = meta[1].strip().replace(' ', '_')
        data_out['data_version'] = int(meta[5].strip())
        data_out['ts_type'] = meta[19].strip().replace(' ', '_')
        data_out['PI_email'] = meta[16].strip().replace(' ', '_')
        data_out['variables'] = vars_to_retrieve 
        #data_out['data_id'] = 'DMS_AMS_CVO'
        # number of sampling heights
        # sampling heights
        # PI?
        
        
        # Add date and time and the rest of the data to a dictionary
        data_out['dtime'] = []
        data_out['vmrdms'] = []
        data_out['vmrdms_nd'] = []
        #data_out['vmrdms_std'] = []
        data_out['vmrdms_flag'] = []
        # CS, REM?
        for i in range(1, len(x)):
            datestring = x[i][0]  + 'T' + x[i][1]
            data_out['dtime'].append(np.datetime64(datestring))
            data_out['vmrdms'].append(np.float(x[i][4]))
            data_out['vmrdms_nd'].append(np.float(x[i][5]))
            #data_out['vmrdms_std'].append(np.float(x[i][6]))
            data_out['vmrdms_flag'].append(np.int(x[i][7]))
            
            
            


        # Comment this because we hace all the variables in the file? 
        
        # dependent on the station, some of the required input variables
        # may not be provided in the data file. These will be ignored
        # in the following list that iterates over all data rows and will
        # be filled below, with vectors containing NaNs after the file 
        # reading loop
        #vars_available = {}
        #for var in vars_to_read:
        #    if var in data_out.keys():
        #        vars_available[var] = data_out.keys[var]
        #    else:
        #        self.logger.warning("Variable {} not available in file {}"
        #                            .format(var, os.path.basename(filename)))



        # Only the data should be converted to arrays
        data_out['vmrdms'] = np.asarray(data_out['vmrdms'])
        data_out['vmrdms_nd'] = np.asarray(data_out['vmrdms_nd'])
        data_out['vmrdms_flag'] = np.asarray(data_out['vmrdms_flag'])
        data_out['dtime'] = np.asarray(data_out['dtime'])
            
            
        #for var in vars_to_read:
        #    if var not in data_out.keys():
        #        array = np.zeros(len(data_out['dtime'])) * np.nan
        #    data_out[var] = array
            
            
        ## Can be commented; we don't need to compute any vars
        # compute additional variables (if applicable)
        # data_out = self.compute_additional_vars(data_out, vars_to_compute)
        
        # convert data vectors to pandas.Series (if applicable)
        if vars_as_series:        
            #for var in (vars_to_read + vars_to_compute):
            #    if var in vars_to_retrieve:
            #        data_out[var] = pd.Series(data_out[var], 
            #                                  index=data_out['dtime'])
            #    else:
            #        del data_out[var]
            for key in data_out:
                if key in vars_to_retrieve:
                    data_out[key] = pd.Series(data_out[key], 
                                              index=data_out['dtime'])
                else:
                    del data_out[key]
                    
            
            
            
            
        #self.logger.debug('The following lines were ignored: {}'.format(
         #       _lines_ignored))   # ???
         
         
        return data_out



    
    
    
    
    

    
    def read(self, vars_to_retrieve=None, files=None, first_file=None, 
             last_file=None):
        """Method that reads list of files as instance of :class:`UngriddedData`
        
        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None, 
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        files : :obj:`list`, optional
            list of files to be read. If None, then the file list is used that
            is returned on :func:`get_file_list`.
        first_file : :obj:`int`, optional
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : :obj:`int`, optional
            index of last file in list to read. If None, the very last file 
            in the list is used
            
        Returns
        -------
        UngriddedData
            data object
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
            
        if files is None:
            if len(self.files) == 0:
                self.get_file_list()  # is already implemented in ReadUngriddedBase !!
            files = self.files
    
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
            
        files = files[first_file:last_file]
        
    
    

    
           
        data_obj = UngriddedData() 
        meta_key = 0.0  # Why 0.0 ??? 
        idx = 0  
        
        #assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx
    
        num_vars = len(vars_to_retrieve)
        num_files = len(files)
        disp_each = int(num_files*0.1)  
        if disp_each < 1:
            disp_each = 1
    
        for i, _file in enumerate(files):
            
            #if i%disp_each == 0:
              #  print_log.info("Reading file {} of {} ({})".format(i, 
               #                  num_files, type(self).__name__))
               
            
            
            station_data = self.read_file(_file, 
                                          vars_to_retrieve=vars_to_retrieve)
            
            
            
            # Fill the metadata dict
            # the location in the data set is time step dependant!
            # use the lat location here since we have to choose one location
            # in the time series plot
            metadata[meta_key] = od()
            metadata[meta_key].update(station_data.get_meta())
            metadata[meta_key].update(station_data.get_station_coords())
            metadata[meta_key]['dataset_name'] = self.DATASET_NAME
            metadata[meta_key]['ts_type'] = self.TS_TYPE
            metadata[meta_key]['variables'] = vars_to_retrieve
            metadata[meta_key]['data_id'] = self.DATA_ID
            if 'instrument_name' in station_data and station_data['instrument_name'] is not None:
                instr = station_data['instrument_name']
            else:
                instr = self.INSTRUMENT_NAME
            metadata[meta_key]['instrument_name'] = instr
            
            # this is a list with indices of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            meta_idx[meta_key] = od()
            
            
            num_times = len(station_data['dtime'])
            
            #access array containing time stamps
            # TODO: check using index instead (even though not a problem here 
            # since all Aerocom data files are of type timeseries)
            times = np.float64(station_data['dtime'])

            totnum = num_times * num_vars
            
            #check if size of data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                #if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)
            
            
            for var_idx, var in enumerate(vars_to_retrieve):
                values = station_data[var]
                start = idx + var_idx * num_times
                stop = start + num_times
                
                
                #write common meta info for this station (data lon, lat and 
                #altitude are set to station locations)
                data_obj._data[start:stop, 
                               data_obj._LATINDEX] = station_data['latitude']
                data_obj._data[start:stop, 
                               data_obj._LONINDEX] = station_data['longitude']
                data_obj._data[start:stop, 
                               data_obj._ALTITUDEINDEX] = station_data['altitude']
                data_obj._data[start:stop, 
                               data_obj._METADATAKEYINDEX] = meta_key
                               
                # write data to data object
                data_obj._data[start:stop, data_obj._TIMEINDEX] = times
                data_obj._data[start:stop, data_obj._DATAINDEX] = values
                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx
                


                    
                meta_idx[meta_key][var] = np.arange(start, stop)
                
                if not var in data_obj.var_idx:
                    data_obj.var_idx[var] = var_idx
                
                
            idx += totnum  
            meta_key = meta_key + 1.
        
        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        data_obj.data_revision[self.DATASET_NAME] = self.data_revision
        self.data = data_obj
        return data_obj
    
if __name__ == "__main__":
     
    r = ReadGAW()
    data = r.read('vmrdms')
    
    print(data.station_name)
    
    
    # data.plot_station_coordinates()
    
    data.plot_station_timeseries(station_name='Amsterdam_Island')
    
    print(data.metadata[0])
    
    
    

    
    
