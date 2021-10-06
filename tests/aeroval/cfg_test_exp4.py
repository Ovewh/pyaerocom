### Very simple setup to make sure the basic stuff works in AeroVal
from pyaerocom import const
import os
TMPDIR = const.LOCAL_TMP_DIR
BASEOUT = os.path.join(TMPDIR, 'aeroval')
os.makedirs(BASEOUT, exist_ok=True)

MODELS = {
    'TM5-AP3-CTRL' : dict(model_id='TM5-met2010_CTRL-TEST',
                          model_ts_type_read='monthly',
                          flex_ts_type=False)
}

OBS_GROUNDBASED = {
    'AERONET-Sun' : dict(obs_id='AeronetSunV3L2Subset.daily',
                         obs_vars = ['od550aer'],
                         obs_vert_type='Column')
    'AN-EEA-MP'         : dict(is_superobs = True,
                               obs_id = ('AeronetSunV3L2Subset.daily',
                                         'AeronetSDAV3L2Subset.daily'),
                               obs_vars = ['od550aer'],
                               obs_vert_type = 'Column',

                               ),

}

CFG = dict(

    model_cfg = MODELS,
    obs_cfg = OBS_GROUNDBASED,

    json_basedir = os.path.join(BASEOUT, 'data'),
    coldata_basedir = os.path.join(BASEOUT, 'coldata'),

    # if True, existing colocated data files will be deleted
    reanalyse_existing = True,
    raise_exceptions = True,
    only_json = False,
    add_model_maps = True,
    only_model_maps = False,

    clear_existing_json = False,

    # Regional filter for analysis
    filter_name = 'WORLD-wMOUNTAINS',

    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type = 'monthly',

    map_zoom = 'World',

    freqs = ['monthly'],
    periods = ['2010'],
    add_seasons=False,
    main_freq = 'monthly',
    zeros_to_nan = False,

    min_num_obs=None,
    colocate_time=False,

    obs_remove_outliers=False,
    add_seasons=False,
    model_remove_outliers=False,
    harmonise_units=True,
    regions_how = 'default'
    annual_stats_constrained=True,

    proj_id = 'test',
    exp_id = 'exp4',
    exp_name = 'AeroVal test experiment 4',
    exp_descr = ('Test superobs processing'),
    exp_pi = 'Jonas Gliss',

    public = True,
)

if __name__=='__main__':
    from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
    from pyaerocom.access_testdata import initialise
    tda = initialise()
    stp = EvalSetup(**CFG)
    ana = ExperimentProcessor(stp)
    ana.run()
    print(ana.exp_output)