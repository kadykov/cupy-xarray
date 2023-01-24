import numpy as np
import pytest
import xarray as xr
from xarray.core.pycompat import DuckArrayModule
from xarray.tests import requires_pint

dask_array_type = DuckArrayModule("dask").type
pint_array_type = DuckArrayModule("pint").type

from pint import UnitRegistry

import cupy_xarray  # noqa: F401

ureg = UnitRegistry()


@pytest.fixture
def tutorial_ds_air():
    return xr.tutorial.load_dataset("air_temperature")


@pytest.fixture
def tutorial_da_air(tutorial_ds_air):
    return tutorial_ds_air.air


@pytest.fixture
def tutorial_ds_air_dask():
    return xr.tutorial.open_dataset("air_temperature", chunks={"lat": 25, "lon": 25, "time": -1})


@pytest.fixture
def tutorial_da_air_dask(tutorial_ds_air_dask):
    return tutorial_ds_air_dask.air


@pytest.fixture
def tutorial_ds_air_pint():
    return xr.tutorial.load_dataset("air_temperature") * ureg.Quantity("degree_Kelvin")


@pytest.fixture
def tutorial_da_air_pint(tutorial_ds_air_pint):
    return tutorial_ds_air_pint.air


@pytest.fixture
def tutorial_ds_air_pint_dask():
    return xr.tutorial.open_dataset(
        "air_temperature", chunks={"lat": 25, "lon": 25, "time": -1}
    ) * ureg.Quantity("degree_Kelvin")


@pytest.fixture
def tutorial_da_air_pint_dask(tutorial_ds_air_pint_dask):
    return tutorial_ds_air_pint_dask.air


def test_data_set_accessor(tutorial_ds_air):
    ds = tutorial_ds_air
    assert hasattr(ds, "cupy")
    assert not ds.cupy.is_cupy

    ds = ds.as_cupy()
    assert ds.cupy.is_cupy

    ds = ds.cupy.as_numpy()
    assert not ds.cupy.is_cupy


def test_data_array_accessor(tutorial_da_air):
    da = tutorial_da_air
    assert hasattr(da, "cupy")
    assert not da.cupy.is_cupy

    da = da.as_cupy()
    assert da.cupy.is_cupy

    garr = da.cupy.get()
    assert isinstance(garr, np.ndarray)

    da = da.cupy.as_numpy()
    assert not da.cupy.is_cupy


def test_data_array_accessor_dask(tutorial_da_air_dask):
    da = tutorial_da_air_dask
    assert hasattr(da, "cupy")
    assert not da.cupy.is_cupy

    da = da.as_cupy()
    assert da.cupy.is_cupy
    assert isinstance(da.data, dask_array_type)

    da = da.cupy.as_numpy()
    assert not da.cupy.is_cupy


@requires_pint
def test_data_array_accessor_pint(tutorial_da_air_pint):
    da = tutorial_da_air_pint
    assert hasattr(da, "cupy")
    assert not da.cupy.is_cupy

    da = da.as_cupy()
    assert da.cupy.is_cupy
    assert isinstance(da.data, pint_array_type)

    da = da.cupy.as_numpy()
    assert not da.cupy.is_cupy
    assert isinstance(da.data, pint_array_type)


@requires_pint
def test_data_array_accessor_pint_dask(tutorial_da_air_pint_dask):
    da = tutorial_da_air_pint_dask
    assert hasattr(da, "cupy")
    assert not da.cupy.is_cupy

    da = da.as_cupy()
    assert da.cupy.is_cupy
    assert isinstance(da.data, pint_array_type)
    assert isinstance(da.data.magnitude, dask_array_type)

    da = da.cupy.as_numpy()
    assert not da.cupy.is_cupy
    assert isinstance(da.data, pint_array_type)
    assert isinstance(da.data.magnitude, dask_array_type)
