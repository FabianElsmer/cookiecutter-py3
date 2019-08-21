import sys
import logging

{%- if cookiecutter.logging|lower == 'logging_py3' %}

from logging_py3 import log
_setup_logging = log.setup_logging

{%- else %}

def _setup_logging(config):
    if config is None:
        config = {}

    config.setdefault('level', logging.DEBUG)
    config.setdefault('stream', sys.stdout)
    logging.basicConfig(**config)

{%- endif %}


def setup_logging(config=None):
    _setup_logging(config)


