# -*- coding: utf-8 -*-

import json
from functools import wraps

from elasticsearch import Elasticsearch

from elasticmock.utilities import generate_key, generate_pretty_key
from elasticmock.exceptions import RequestNotFound
from elasticmock.elasticrecorder import ElasticRecorder

def load_from_file(file_name):
    path = './test/fixtures/es/{}'.format(file_name)

    result = None
    with open(path, 'r') as f:
        result = json.loads(f.read())

    return result

def load_persisted(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = generate_key(*args, **kwargs)
        file_name = "{}_{}".format(Replayer.scope, key)
        try:
            result = load_from_file(file_name)
        except (OSError, IOError) as e:
            raise RequestNotFound(
                "No recorded request for file '{}' with request: {}".format(
                    file_name,
                    generate_pretty_key(*args, **kwargs)))
        
        return result
    return decorated

class Replayer(Elasticsearch, ElasticRecorder):

    def __init__(self, *args, **kwargs):
        pass#super().__init__()

    @load_persisted
    def exists(self, *args, **kwargs):
        pass#super().get(*args, **kwargs)

    @load_persisted
    def get(self, *args, **kwargs):
        pass#super().get(*args, **kwargs)

    @load_persisted
    def get_source(self, *args, **kwargs):
        pass#super().get(*args, **kwargs)

    @load_persisted
    def count(self, *args, **kwargs):
        pass#super().get(*args, **kwargs)

    @load_persisted
    def scan(self, *args, **kwargs):
        pass#super().get(*args, **kwargs)

    @load_persisted
    def search(self, *args, **kwargs):
        pass#super().get(*args, **kwargs)

    @load_persisted
    def suggest(self, *args, **kwargs):
        pass#super().get(*args, **kwargs)
