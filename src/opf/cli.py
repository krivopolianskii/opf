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
    '--test', is_flag=True, help='Running in test environment')
def runopt(**kwargs):
    """Run optimization
    """
    model.runopt()

