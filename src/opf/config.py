# -*- coding: utf-8 -*-

"""Configuration parameters
"""

import logging

objects = ['obj1', 'obj2', 'obj3', 'obj4', 'obj5']
stations = ['st1', 'st2', 'st3']
processing_time = {
    ('obj1', 'st1'): 10,
    ('obj2', 'st1'): 20,
    ('obj3', 'st1'): 40,
    ('obj4', 'st1'): 10,
    ('obj5', 'st1'): 25,
    ('obj1', 'st2'): 43,
    ('obj2', 'st2'): 12,
    ('obj3', 'st2'): 53,
    ('obj4', 'st2'): 24,
    ('obj5', 'st2'): 12,
    ('obj1', 'st3'): 42,
    ('obj2', 'st3'): 32,
    ('obj3', 'st3'): 20,
    ('obj4', 'st3'): 20,
    ('obj5', 'st3'): 20
}

max_process_time = 8 * 60
large_value = 1e5


def setup_logger():
    """Configure logger
    """
    logger = logging.getLogger('opf')

    # set stream handler format
    stream_formatter = logging.Formatter(
        '%(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # add stdout handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger


