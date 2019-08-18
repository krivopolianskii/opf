# -*- coding: utf-8 -*-

"""Library interface
"""

from opf import config
from opf.models import *

def run():
    """Run optimization
    """

    objects = config.objects
    stations = config.stations
    processing_time = config.processing_time

    model = SimpleModel(
        objects, stations, processing_time
    )
    output = []
    if model.is_optimal():
        results = model.get_results()
        for i, row in results.iterrows():
            if row.station == stations[0]:
                output.append(row.object)

    return output

