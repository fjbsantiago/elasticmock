# -*- coding: utf-8 -*-
from functools import wraps
from contextlib import ExitStack
from elasticsearch.client import _normalize_hosts
from mock import patch

from elasticmock.fake_elasticsearch import FakeElasticsearch
from elasticmock.recorder import Recorder
from elasticmock.replayer import Replayer

ELASTIC_INSTANCES = {}

def _get_elasticmock(hosts=None, *args, **kwargs):
    host = _normalize_hosts(hosts)[0]
    elastic_key = '{0}:{1}'.format(
        host.get('host', 'localhost'), host.get('port', 9200)
    )

    if elastic_key in ELASTIC_INSTANCES:
        connection = ELASTIC_INSTANCES.get(elastic_key)
    else:
        connection = FakeElasticsearch()
        ELASTIC_INSTANCES[elastic_key] = connection
    return connection

def elasticmock(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ELASTIC_INSTANCES.clear()
        with patch('elasticsearch.Elasticsearch', _get_elasticmock):
            result = f(*args, **kwargs)
        return result
    return decorated

def record(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        Recorder.scope = f.__name__
        with patch('elasticsearch.Elasticsearch', Recorder):
            result = f(*args, **kwargs)
        return result
    return decorated

def replay(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        Replayer.scope = f.__name__
        with patch('elasticsearch.Elasticsearch', Replayer):
            result = f(*args, **kwargs)
        return result
    return decorated
