from pyaerocom._lowlevel_helpers import (BrowseDict, ListOfStrings, DictType,
                                         StrType)
from pyaerocom.aeroval.aux_io_helpers import check_aux_info
from pyaerocom.aeroval._lowlev import EvalEntry

class ModelEntry(EvalEntry, BrowseDict):
    """Modeln configuration for evaluation (dictionary)

    Note
    ----
    Only :attr:`model_id` is mandatory, the rest is optional.

    Attributes
    ----------
    model_id : str
        ID of model run in AeroCom database (e.g. 'ECMWF_CAMS_REAN')
    model_ts_type_read : str or dict, optional
        may be specified to explicitly define the reading frequency of the
        model data. Not to be confused with :attr:`ts_type`, which specifies
        the frequency used for colocation. Can be specified variable specific
        by providing a dictionary.
    model_use_vars : dict
        dictionary that specifies mapping of model variables. Keys are
        observation variables, values are strings specifying the corresponding
        model variable to be used
        (e.g. model_use_vars=dict(od550aer='od550csaer'))
    model_add_vars : dict
        dictionary that specifies additional model variables. Keys are
        observation variables, values are lists of strings specifying the
        corresponding model variables to be used
        (e.g. model_use_vars=dict(od550aer=['od550csaer', 'od550so4']))
    model_read_aux : dict
        may be used to specify additional computation methods of variables from
        models. Keys are obs variables, values are dictionaries with keys
        `vars_required` (list of required variables for computation of var
        and `fun` (method that takes list of read data objects and computes
        and returns var)
    """
    model_id = StrType()
    model_use_vars = DictType()
    model_add_vars = DictType()
    model_read_aux = DictType()

    def __init__(self, model_id, **kwargs):
        self.model_id = model_id
        self.model_ts_type_read = ''
        self.model_use_vars = {}
        self.model_add_vars = {}
        self.model_read_aux = {}

        self.update(**kwargs)
        self.check_cfg()

    def get_all_vars(self):
        muv = list(self.model_use_vars.values())
        mav = list(self.model_add_vars.values())
        mra = list(self.model_read_aux.keys())
        return list(set(muv + mav + mra))

    def check_cfg(self):
        """Check that minimum required attributes are set and okay"""
        assert isinstance(self.model_id, str)
        assert isinstance(self.model_add_vars, dict)
        assert isinstance(self.model_use_vars, dict)
        assert isinstance(self.model_read_aux, dict)
        for key, val in self.model_add_vars.items():
            assert isinstance(val, list)
        for key, val in self.model_use_vars.items():
            assert isinstance(val, str)

    def _check_update_aux_funcs(self, funcs):
        mra = {}
        for var, aux_info in self.model_read_aux.items():
            mra[var] = check_aux_info(funcs=funcs, **aux_info)
        self.model_read_aux = mra
