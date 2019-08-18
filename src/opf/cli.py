# -*- coding: utf-8 -*-

"""Command line interface
"""

import click

from opf import config
from opf.models import *

logger = config.setup_logger()


@click.group()
def opf():
    """One-piece-flow model
    """


@opf.command()
@click.option(
    '--verbose', is_flag=True, help='Verbosity mode')
@click.option(
    '--maxtime', default=None, type=int, help='Maximal flow time (minutes)')
def model(**kwargs):
    """Run optimization
    """
    verbose = kwargs.get('verbose')
    max_time = kwargs.get('maxtime', config.max_process_time)

    objects = config.objects
    stations = config.stations
    processing_time = config.processing_time

    logger.info('model started')

    model = SimpleModel(
        objects, stations, processing_time,
        verbose=verbose,
        max_flow_time=max_time
    )

    logger.info('model completed')

    if model.is_optimal():
        results = model.get_results()
        for i, row in results.iterrows():
            logger.info(
                f'object {row.object} on {row.station} is '
                f'processing from {row.start:.1f} to {row.end:.1f}')

        logger.info('')
        logger.info(f'flow processing time: {model.get_obj_val():.0f}')
    else:
        logger.info('solution has not been found')

