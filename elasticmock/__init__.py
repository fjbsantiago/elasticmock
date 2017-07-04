# -*- coding: utf-8 -*-
from functools import wraps
from contextlib import ExitStack
from elasticsearch.client import _normalize_hosts
from mock import patch

from elasticmock.fake_elasticsearch import FakeElasticsearch
from elasticmock.record_elasticsearch import RecordElasticsearch
from elasticmock.recorded_elasticsearch import RecordedElasticsearch

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



    ADD function name to response files name to make it easier to know which files were created by which test

def elasticmock(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ELASTIC_INSTANCES.clear()
        with patch('elasticsearch.Elasticsearch', _get_elasticmock):
            result = f(*args, **kwargs)
        return result
    return decorated

def elasticrecord(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print('Recording this guy: {}'.format(f.func_name))
        with patch('elasticsearch.Elasticsearch', RecordElasticsearch):
            result = f(*args, **kwargs)
        return result
    return decorated

def elasticrecorded(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        with patch('elasticsearch.Elasticsearch', RecordedElasticsearch):
            result = f(*args, **kwargs)
        return result
    return decorated