# -*- coding: utf-8 -*-

"""Testing models
"""

import pytest

from opf.models import *


@pytest.fixture(scope='module')
def model_data():
    class ModelData:
        objects = ['obj']
        stations = ['station']
        processing_time = {('obj', 'station'): 10}
    return ModelData()


def test_simple_model(model_data):
    model = SimpleModel(
        model_data.objects,
        model_data.stations,
        model_data.processing_time)

    assert abs(model.get_obj_val() - 10) < 1e-3


def test_max_time(model_data):
    model = SimpleModel(
        model_data.objects,
        model_data.stations,
        model_data.processing_time,
        max_flow_time=12)
    assert model.is_optimal()

    model = SimpleModel(
        model_data.objects,
        model_data.stations,
        model_data.processing_time,
        max_flow_time=8)
    assert not model.is_optimal()

