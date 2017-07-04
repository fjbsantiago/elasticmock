# -*- coding: utf-8 -*-

import random
import string
import hashlib
import collections

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
        self.sort_dict_recursively(self)

    def __setitem__(self, k, v):
        if isinstance(v, dict):
            v = RecursivelySortedDict(v)

        super().__setitem__(k, v)

    def sort_dict_recursively(self, obj):
        for k, v in obj.items():

            if isinstance(v, dict):
                obj[k] = RecursivelySortedDict(v)

            elif isinstance(v, collections.Iterable):
                self.sort_items_recursively(v)

    def sort_items_recursively(self, items):
        for item in items:

            if isinstance(item, dict):
                self.sort_dict_recursively(item)

            elif not isinstance(item, str) and isinstance(item, collections.Iterable):
                self.sort_items_recursively(item)

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
    return hashlib.md5(generate_str_key(**kwargs).encode()).hexdigest()
