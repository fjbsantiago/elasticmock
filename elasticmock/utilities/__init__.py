# -*- coding: utf-8 -*-

import random
import string
import hashlib

from sortedcontainers import SortedDict

DEFAULT_ELASTICSEARCH_ID_SIZE = 20
CHARSET_FOR_ELASTICSEARCH_ID = string.ascii_letters + string.digits

def get_random_id(size=DEFAULT_ELASTICSEARCH_ID_SIZE):
    return ''.join(random.choice(CHARSET_FOR_ELASTICSEARCH_ID) for _ in range(size))

class RecursivelySortedDict(SortedDict):
    """The keys of this dictionary and keys of any child dictionaries
    are always sorted.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sort_self_recursively()

    def __setitem__(self, k, v):
        if isinstance(v, dict):
            v = RecursivelySortedDict(v)

        super().__setitem__(k, v)

    def sort_self_recursively(self):
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = RecursivelySortedDict(v)

def generate_str_key(*args, **kwargs):
    """Converts elastic search kwargs into its string representation
    and joins them into one single string.
    Dictionaries are converted to RecursivelySortedDict because of
    their naturally unpredictable order. 
    """

    return ''.join((
                str(kwargs.get('index')),
                str(kwargs.get('doc_type')),
                str(RecursivelySortedDict(kwargs.get('body', {}))),
                str(RecursivelySortedDict(kwargs.get('query', {})))))

def generate_pretty_key(*args, **kwargs):
    """Same as generate_str_key(), except the key is formated to
    make debugging easier
    """
    return '\n'.join((
        "",
        "\tindex: {}".format(str(kwargs.get('index'))),
        "\tdoc_type: {}".format(str(kwargs.get('doc_type'))),
        "\tbody: {}".format(str(RecursivelySortedDict(kwargs.get('body')))),
        "\tquery: {}".format(str(RecursivelySortedDict(kwargs.get('query')))),
        ))

def generate_key(*args, **kwargs):
    """Converts key to md5 hash and returns it as a string 
    """
    print('===================================================')
    print(generate_str_key(**kwargs))
    print('===================================================')
    return hashlib.md5(generate_str_key(**kwargs).encode()).hexdigest()
