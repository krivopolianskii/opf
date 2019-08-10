# -*- coding: utf-8 -*-

"""Optimization models
"""

import abc
import logging

import pandas as pd
import pyscipopt

from opf import config

logger = logging.getLogger('opf')

__all__ = ['SimpleModel']


class ModelBase(abc.ABC):
    def __init__(self, objects, stations, processing_time, **kwargs):
        # list of objects
        self.objects = objects
        # list of stations
        self.stations = stations
        # processing time dict
        self.processing_time = processing_time
        # maximal flow time
        self.max_flow_time = kwargs.get('max_flow_time', 480)
        # verbose mode
        self.verbose = kwargs.get('verbose', False)

        # init model
        self.model = pyscipopt.Model()

        # init variables
        self.start_time = self.init_start_time_var()
        self.end_time = self.init_end_time_var()
        self.delta = self.init_delta_var()

        # constraints
        self.add_last_station_cons()
        self.add_objects_order_cons()
        self.add_stations_cons()

        # objective function
        self.set_objective()

        # run optimization
        self.optimize()

    @abc.abstractmethod
    def init_start_time_var(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def init_end_time_var(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def init_delta_var(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def add_last_station_cons(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def add_objects_order_cons(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def add_stations_cons(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def set_objective(self):
        raise NotImplementedError()

    def optimize(self):
        if not self.verbose:
            self.model.hideOutput()
        self.model.optimize()

    def is_optimal(self):
        return self.model.getStatus() == 'optimal'

    def get_results(self):
        lol = []

        for i, obj in enumerate(self.objects):
            for j, station in enumerate(self.stations):
                start = self.model.getVal(self.start_time[i, j])
                lol += [[obj, station, start, start + self.processing_time[obj, station]]]

        results = pd.DataFrame(lol)
        results.columns = ['object', 'station', 'start', 'end']
        results.sort_values(by=['start'], inplace=True)

        return results

    def get_obj_val(self):
        return self.model.getObjVal()


class SimpleModel(ModelBase):
    def __init__(self, objects, stations, processing_time, **kwargs):
        super().__init__(objects, stations, processing_time, **kwargs)

    def init_start_time_var(self):
        start_time = {}
        for i, _ in enumerate(self.objects):
            for j, _ in enumerate(self.stations):
                start_time[i, j] = self.model.addVar(vtype='C', lb=0, ub=self.max_flow_time)
        return start_time

    def init_end_time_var(self):
        return self.model.addVar(vtype='C', lb=0, ub=self.max_flow_time)

    def init_delta_var(self):
        delta = {}
        for i1, _ in enumerate(self.objects):
            for i2, _ in enumerate(self.objects):
                if i1 == i2:
                    continue
                for j, _ in enumerate(self.stations):
                    delta[i1, i2, j] = self.model.addVar(vtype='B')
        return delta

    def add_last_station_cons(self):
        last_station_index = len(self.stations) - 1
        for i, obj in enumerate(self.objects):
            self.model.addCons(
                self.start_time[i, last_station_index] +
                self.processing_time[obj, self.stations[-1]] <= self.end_time)

    def add_objects_order_cons(self):
        for i, obj in enumerate(self.objects):
            for j, station in enumerate(self.stations[:-1]):
                self.model.addCons(
                    self.start_time[i, j] - self.start_time[i, j+1] +
                    self.processing_time[obj, station] <= 0)

    def add_stations_cons(self):
        for i1, obj1 in enumerate(self.objects):
            for i2, obj2 in enumerate(self.objects):
                if i1 == i2:
                    continue
                for j, station in enumerate(self.stations):
                    self.model.addCons(
                        self.start_time[i1, j] + self.processing_time[obj1, station] <=
                        self.start_time[i2, j] + config.large_value * self.delta[i1, i2, j])
                    self.model.addCons(
                        self.start_time[i2, j] + self.processing_time[obj2, station] <=
                        self.start_time[i1, j] + config.large_value * (1 - self.delta[i1, i2, j]))

    def set_objective(self):
        self.model.setObjective(self.end_time)


