# -*- coding: utf-8 -*-

import json
from functools import wraps

#from elasticsearch import Elasticsearch
from elasticsearch.client.utils import query_params
from elasticsearch.exceptions import NotFoundError

from elasticmock.utilities import get_random_id, generate_key, generate_pretty_key
from elasticmock.exceptions import RequestNotFound
from elasticmock.fake_elasticsearch import FakeElasticsearch

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
        
        try:
            result = load_from_file(key)
        except (OSError, IOError) as e:
            raise RequestNotFound(
                'No recorded request for: {}'.format(generate_pretty_key(*args, **kwargs)))
        
        return result
    return decorated

class RecordedElasticsearch(FakeElasticsearch):

    def __init__(self, *args, **kwargs):
        super().__init__()

    @load_persisted
    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)

    @load_persisted
    def get_source(self, *args, **kwargs):
        super().get(*args, **kwargs)

    @load_persisted
    def count(self, *args, **kwargs):
        super().get(*args, **kwargs)

    @load_persisted
    def search(self, *args, **kwargs):
        super().get(*args, **kwargs)

    @load_persisted
    def suggest(self, *args, **kwargs):
        super().get(*args, **kwargs)