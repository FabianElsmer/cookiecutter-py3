import logging

import yacm
import asyncio
from aiohttp import web


from .handlers import routes

from .plugins import cors
{%- if cookiecutter.database | lower == 'mongodb' %}
from .plugins import mongo
{%- endif %}


class Application(web.Application):
    def __init__(self, extra_config=None, **kwargs):
        super(Application, self).__init__(**kwargs)
        self.config = yacm.read_configs('{{ cookiecutter.project_slug }}')

        if extra_config.get('incremental', True):
            yacm.merge(self.config, extra_config)
        else:
            self.config = extra_config

        self.load_plugins()
        routes.register(self)

    def load_plugins(self):
        {%- if cookiecutter.database | lower == 'mongodb' %}
        self.cleanup_ctx.append(mongo.enable)
        {%- endif %}

        # run enable cors as the last step inside cleanup context
        # as other plugins might register new routes
        self.cleanup_ctx.append(cors.enable)


# used for aiohttp-devtools
def create_app(loop=None, extra_config=None):
    if loop is None:
        logging.basicConfig(level=logging.DEBUG)
        loop = asyncio.get_event_loop()

    return Application(loop=loop, extra_config=extra_config)
