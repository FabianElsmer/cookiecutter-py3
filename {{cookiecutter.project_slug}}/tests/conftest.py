import asyncio
import pytest
import argparse
import socket

{%- if cookiecutter.database|lower == 'mongodb' %}

import dockerdb.mongo_pytest

{%- endif %}

from {{ cookiecutter.project_slug }}.app import create_app

{%- if cookiecutter.database|lower == 'mongodb' %}

def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


# required to add port option to pytest cli
# CI is not happy with non standard port 27017 so we need a way to specify it
def pytest_addoption(parser):
    parser.addoption("--port", action="store", help="Specify mongodb port, use 0 for next free port")

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', type=int, default=27017)

args, unknown = parser.parse_known_args()
port = args.port
if port < 1:
    port = get_free_tcp_port()

db_name = 'test'
DATA = {
    db_name: {},
}

client_args = {
    'socketTimeoutMS': 2000,
    'connectTimeoutMS': 2000
}

# DockerDB Mongo fixture resets the test data before every new test
mongo = dockerdb.mongo_pytest.mongo_fixture(versions=["3.6.8"],
                                            data=DATA,
                                            port=port,
                                            client_args=client_args)

@pytest.yield_fixture(scope='function')
def motor_client(mongo):
    yield mongo.asyncio_client()

@pytest.yield_fixture(scope='function')
def database(motor_client):
    yield motor_client[db_name]

{%- endif %}

@pytest.fixture(scope='function')
def config(mongo):
    {%- if cookiecutter.database | lower == 'mongodb' %}
    mongo_host = mongo.ip_address()
    {%- endif %}

    return {
        {%- if cookiecutter.database | lower == 'mongodb' %}
        'mongodb': {
            'default': {
                'uri': 'mongodb://{}:{}/{}'.format(
                    mongo_host, port, db_name),
                'host': mongo_host,
                'port': port,
                'database': db_name
            }
        },
        {%- endif %}
        'cors':{
            'origins': ['http://127.0.0.1']
        },
        'incremental': False
    }

@pytest.yield_fixture(scope='function')
def loop():
    """
    Create an instance of the default event loop for each test case.
    Prevents leaking of tasks through shared event loops
    Prevents RuntimeError: web.Application instance initialized with different loop
    """

    loop = asyncio.get_event_loop_policy().new_event_loop()

    # Make sure we have one global event loop
    asyncio.set_event_loop(loop)

    yield loop

    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()

@pytest.yield_fixture(scope='function')
def client(aiohttp_client, app):
    c = aiohttp_client(app)
    yield c
    c.close()

@pytest.fixture(scope='function')
def app(loop, config):
    return create_app(loop=loop, extra_config=config)
