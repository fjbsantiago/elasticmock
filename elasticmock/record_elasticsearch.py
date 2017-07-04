import json
import hashlib
from functools import wraps
from unittest import TestCase

from elasticsearch import Elasticsearch

from elasticmock.utilities import generate_key

def save_to_file(file_name, data):
    path = './test/fixtures/es/{}'.format(file_name)
    serialized = json.dumps(data)
    with open(path, 'w') as f:
        f.write(serialized)

def persist(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        key = generate_key(*args, **kwargs)
        file_name = "{}_{}".format(RecordElasticsearch.scope, key)
        save_to_file(file_name, result)

        return result
    return decorated

class RecordElasticsearch(Elasticsearch):
    # Identifies the test function used to invoke the class
    scope = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @persist
    def exists(self, *args, **kwargs):
        return super().exists(*args, **kwargs)

    @persist
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    @persist
    def get_source(self, *args, **kwargs):
        return super().get_source(*args, **kwargs)

    @persist
    def count(self, *args, **kwargs):
        return super().count(*args, **kwargs)

    @persist
    def scan(self, *args, **kwargs):
        return super().scan(*args, **kwargs)

    @persist
    def search(self, *args, **kwargs):
        return super().search(*args, **kwargs)

    @persist
    def suggest(self, *args, **kwargs):
        return super().suggest(*args, **kwargs)
