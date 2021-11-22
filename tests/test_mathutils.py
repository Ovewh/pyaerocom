import numpy as np
import pytest
from numpy.testing import assert_allclose

from pyaerocom.aux_var_helpers import vmrx_to_concx
from pyaerocom.mathutils import (
    _nanmean_and_std,
    calc_statistics,
    estimate_value_range,
    exponent,
    is_strictly_monotonic,
    make_binlist,
)


@pytest.mark.parametrize(
    "inputval,p,T,vmr_unit,mmol_var,mmol_air,to_unit,desired",
    [
        (1, 101300, 293, "nmol mol-1", 48, None, "ug m-3", 1.9959),
        (1, 101300, 273, "nmol mol-1", 48, None, "ug m-3", 2.1421),
        (1, 101300, 273, "nmol mol-1", 48, None, "kg m-3", 2.1421e-9),
        (1, 101300, 273, "mol mol-1", 48, None, "kg m-3", 2.1421),
        (1, 98000, 273, "mol mol-1", 48, None, "kg m-3", 2.0724),
    ],
)
def test_vmrx_to_concx(inputval, p, T, vmr_unit, mmol_var, mmol_air, to_unit, desired):
    val = vmrx_to_concx(inputval, p, T, vmr_unit, mmol_var, mmol_air, to_unit)
    assert_allclose(val, desired, rtol=1e-4)


@pytest.mark.parametrize("vmin, vmax, num", [(0, 1, 10), (0.345, 0.346, 100), (-2, -10, 5)])
def test_make_binlist(vmin, vmax, num):
    bins = make_binlist(vmin, vmax, num)
    assert isinstance(bins, list)
    assert bins[0] == vmin
    assert bins[-1] == vmax
    assert len(bins) == num + 1


@pytest.mark.parametrize(
    "inputval,result", [([1, 2], True), ([1], True), ([1, 2, 2], False), ([3, 2], False)]
)
def test_is_strictly_monotonic(inputval, result):
    assert is_strictly_monotonic(inputval) == result


@pytest.mark.parametrize("inputval, desired", [(0.01, -2), (4, 0), (234, 2)])
def test_exponent(inputval, desired):
    assert exponent(inputval) == desired


@pytest.mark.parametrize(
    "data,expected",
    [
        ([1], (1, 0)),
        (np.asarray([1]), (1, 0)),
        ([1, np.nan], (1, 0)),
        ([np.nan, np.nan], (np.nan, np.nan)),
        (np.random.normal(loc=3, scale=0.01, size=100000), (3, 0.01)),
        ([1, np.nan, 0, 2], (1, 0.816497)),
    ],
)
def test__nanmean_and_std(data, expected):
    mean, std = _nanmean_and_std(data)
    mean_, std_ = expected
    if np.isnan(mean_):
        assert np.isnan(mean)
    else:
        assert_allclose(mean, mean_, atol=0.001, rtol=1e-2)
    if np.isnan(std_):
        assert np.isnan(std)
    else:
        assert_allclose(std, std_, atol=0.001, rtol=1e-2)


perfect_stats_num1_mean1 = {
    "totnum": 1,
    "num_valid": 1,
    "refdata_mean": 1,
    "refdata_std": 0,
    "data_mean": 1,
    "data_std": 0,
    "weighted": False,
    "rms": 0,
    "nmb": 0,
    "mnmb": 0,
    "fge": 0,
    "R": np.nan,
    "R_kendall": np.nan,
    "R_spearman": np.nan,
}
perfect_stats_num2_mean1 = perfect_stats_num1_mean1.copy()
perfect_stats_num2_mean1.update(totnum=2)

num_fakedata = 1000
zero_signal = np.zeros(num_fakedata)
noise = np.random.normal(loc=0, scale=0.01, size=num_fakedata)

idx = np.linspace(0, 2 * np.pi, num_fakedata)
sin_signal = np.sin(idx)


@pytest.mark.parametrize(
    "data,ref_data,expected",
    [
        ([1], [1], perfect_stats_num1_mean1),
        ([1, np.nan], [1, np.nan], perfect_stats_num2_mean1),
        (
            zero_signal,
            zero_signal,
            {
                "totnum": 1000.0,
                "num_valid": 1000.0,
                "refdata_mean": 0.0,
                "refdata_std": 0,
                "data_mean": 0.0,
                "data_std": 0,
                "weighted": False,
                "rms": 0.0,
                "R": np.nan,
                "R_spearman": np.nan,
                "R_kendall": np.nan,
                "nmb": 0,
                "mnmb": np.nan,
                "fge": np.nan,
            },
        ),
        (
            zero_signal,
            noise,
            {
                "totnum": 1000.0,
                "num_valid": 1000.0,
                "refdata_mean": 0.0,
                "refdata_std": 0,
                "data_mean": 0.0,
                "data_std": 0,
                "weighted": False,
                "rms": 0.0,
                "R": np.nan,
                "R_spearman": np.nan,
                "R_kendall": np.nan,
                "nmb": -1,
                "mnmb": -2,
                "fge": 2,
            },
        ),
        (
            sin_signal,
            sin_signal,
            {
                "totnum": 1000.0,
                "num_valid": 1000.0,
                "refdata_mean": 0.0,
                "refdata_std": 0.71,
                "data_mean": 0.0,
                "data_std": 0.71,
                "weighted": False,
                "rms": 0.0,
                "R": 1.0,
                "R_spearman": 1.0,
                "R_kendall": 1.0,
                "nmb": 0,
                "mnmb": np.nan,
                "fge": np.nan,
            },
        ),
    ],
)
def test_calc_statistics(data, ref_data, expected):
    stats = calc_statistics(data, ref_data)
    assert isinstance(stats, dict)
    assert len(stats) == len(expected)
    for key, val in expected.items():
        assert key in stats
        assert_allclose(stats[key], val, atol=0.02, rtol=0.01)


def test_calc_statistics_error():
    with pytest.raises(IndexError) as e:
        calc_statistics([1], [1, np.nan])
    assert str(e.value).startswith("boolean index did not match indexed array")


@pytest.mark.parametrize(
    "vmin,vmax,extend_percent,result",
    [
        (0, 1, 0, (0, 1)),
        (-0.012, 3.12345666, 0, (-0.02, 3.13)),
        (-0.012, 3.12345666, 5, (-0.2, 3.3)),
    ],
)
def test_estimate_value_range(vmin, vmax, extend_percent, result):
    vals = estimate_value_range(vmin, vmax, extend_percent)
    assert_allclose(vals, result, rtol=1e-3)


def test_estimate_value_range_error():
    with pytest.raises(ValueError) as e:
        estimate_value_range(0, 0)
    assert str(e.value) == "vmax needs to exceed vmin"
