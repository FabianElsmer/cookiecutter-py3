"""Console script for {{cookiecutter.project_slug}}."""
from .setup_logging import setup_logging
setup_logging()

import sys
import click
import logging

LOG = logging.getLogger(__name__)


@click.command()
def main(args=None):
    """Console script for {{cookiecutter.project_slug}}."""
    click.echo("Replace this message in the cli.py")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
