import pytest
from pyaerocom.conftest import lustre_unavail, testdata_unavail
from pyaerocom.io.read_emep import ReadEMEP, ts_type_from_filename
from pyaerocom.griddeddata import GriddedData
from pyaerocom.colocation import colocate_gridded_gridded
from pyaerocom.colocation import ColocatedData


def test_read_emep():
    r = ReadEMEP()
    assert r.data_id == None
    assert r.vars_provided == []
    assert r.filepath == None

@testdata_unavail
def test_read_emep_data(path_emep):
    path = path_emep['daily']
    print(path)
    r = ReadEMEP(filepath=path)

    # r.filepath = path
    vars_provided = r.vars_provided
    assert isinstance(vars_provided, list)
    assert r.vars_provided == ['vmro3']

    data = r.read_var('vmro3', ts_type='daily')
    assert isinstance(data, GriddedData)
    assert data.time.long_name == 'time'
    assert data.time.standard_name == 'time'

    # # TODO: Compare against expected formats for colocation gridded_gridded, gridded_ungridded
    # # TODO: Read auxilliary variable
    # # TODO: run these two similiar tests parameterized
    # data = r.read_var('vmro3', ts_type='monthly')
    # assert isinstance(data, GriddedData)
    # assert data.time.long_name == 'time'
    # assert data.time.standard_name == 'time'
    # assert data.metadata['computed'] == True

    # data = r.read_var('od550aer', ts_type='monthly')
    # assert data.units == '1'

@testdata_unavail
def test_read_emep_directory(path_emep):
    data_dir = path_emep['data_dir']
    r = ReadEMEP(data_dir=data_dir)
    assert r.data_dir == data_dir
    vars_provided = r.vars_provided
    assert 'vmro3' in vars_provided
    assert 'concpm10' in vars_provided
    assert 'concno2' in vars_provided
    paths = r._get_paths()
    assert len(paths) == 3



@testdata_unavail
def test_read_emep_colocate_gridded_gridded(data_tm5, path_emep):
    filepath = path_emep['monthly']
    r = ReadEMEP(path_emep['monthly'])
    data_emep = r.read_var('concpm10', ts_type='monthly')

    # Change units and year to match TM5 data
    data_emep.change_base_year(2010)
    data_emep.units = '1'
    col = colocate_gridded_gridded(data_emep, data_tm5)
    assert isinstance(col, ColocatedData)

@testdata_unavail
def test_read_emep_colocate_gridded_ungridded(path_emep, some_obs_dataset):
    # Test colcation against some ungridded data
    pass


@pytest.mark.parametrize('filename,ts_type', [
    ('Base_month.nc', 'monthly'),
    ('Base_day.nc', 'daily'),
    ('Base_fullrun', 'yearly')
    ])
def test_ts_type_from_filename(filename, ts_type):
    assert ts_type_from_filename(filename) == ts_type


def test_preprocess_units():
    units = ''
    prefix = 'AOD'
    assert ReadEMEP().preprocess_units(units, prefix) == '1'

    units = 'mgS/m2'
    catch_error = False
    try:
        ReadEMEP().preprocess_units(units)
    except NotImplementedError as e:
        catch_error = True
    assert catch_error == True
