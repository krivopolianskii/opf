

import logging

import pandas as pd
import pyscipopt

from opf import config

# logger = config.setup_logger()
logger = logging.getLogger('opf')


def runopt(verbose=True):
    logger.info(f'model started')
    model = pyscipopt.Model()

    end_time = model.addVar(vtype='C', lb=0, ub=config.max_process_time)
    start_time = init_start_time(model)
    delta = init_delta(model)

    model = init_last_station_constraints(model, start_time, end_time)
    model = init_order_constraints(model, start_time)
    model = init_station_constraints(model, start_time, delta)
    model.setObjective(end_time)

    if not verbose:
        model.hideOutput()

    model.optimize()

    if model.getStatus() == 'optimal':
        results = display_results(model, start_time)
        for _, row in results.iterrows():
            logger.info(
                f'object {row.object} on station {row.station}: '
                f'processing from {row.start:.1f} to {row.end:.1f}')


def init_start_time(model):
    start_time = {}
    for i, obj in enumerate(config.objects):
        for j, station in enumerate(config.stations):
            start_time[i, j] = model.addVar(vtype='C', lb=0, ub=config.max_process_time)
    return start_time


def init_delta(model):
    delta = {}
    for i1, _ in enumerate(config.objects):
        for i2, _ in enumerate(config.objects):
            if i1 == i2:
                continue
            for j, _ in enumerate(config.stations):
                delta[i1, i2, j] = model.addVar(vtype='B')
    return delta


def init_last_station_constraints(model, start_time, end_time):
    last_station_index = len(config.stations) - 1
    for i, obj in enumerate(config.objects):
        model.addCons(start_time[i, last_station_index] + config.processing_time[obj, config.stations[-1]] <= end_time)
    return model


def init_order_constraints(model, start_time):
    for i, obj in enumerate(config.objects):
        for j, station in enumerate(config.stations[:-1]):
            model.addCons(start_time[i, j] - start_time[i, j+1] + config.processing_time[obj, station] <=0)
    return model


def init_station_constraints(model, start_time, delta):
    for i1, obj1 in enumerate(config.objects):
        for i2, obj2 in enumerate(config.objects):
            if i1 == i2:
                continue
            for j, station in enumerate(config.stations):
                model.addCons(
                    start_time[i1, j] + config.processing_time[obj1, station] <=
                    start_time[i2, j] + config.large_value*delta[i1, i2, j])
                model.addCons(
                    start_time[i2, j] + config.processing_time[obj2, station] <=
                    start_time[i1, j] + config.large_value*(1-delta[i1, i2, j]))
    return model


def display_results(model, start_time):
    lol = []
    for i, obj in enumerate(config.objects):
        for j, station in enumerate(config.stations):
            start = model.getVal(start_time[i, j])
            lol += [[obj, station, start, start+config.processing_time[obj, station]]]
            # logger.info(f'object {obj} started on {station} at {start:.1f}')
            # logger.info(f'object {obj} finished on {station} at {start+config.processing_time[obj, station]:.1f}')
    results = pd.DataFrame(lol)
    results.columns = ['object', 'station', 'start', 'end']
    results.sort_values(by=['start'], inplace=True)
    return results
