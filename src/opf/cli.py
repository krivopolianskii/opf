# -*- coding: utf-8 -*-

"""Command line interface
"""

import click

from opf import config
from opf import model

logger = config.setup_logger()


@click.group()
def opf():
    """One-piece-flow model
    """


@opf.command()
@click.option(
    '--verbose', is_flag=True, help='Running in test environment')
def runopt(**kwargs):
    """Run optimization
    """
    verbose = kwargs.get('verbose')

    model.runopt(verbose=verbose)

