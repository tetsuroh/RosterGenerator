# -*- coding: utf-8 -*-
import re


def string_filter(s, fn):
    """
    >>> string_filter("hoge", lambda x: x != 'h')
    "oge"
    """
    return "".join([c for c in s if fn(c)])


def remove_space(s):
    """
    >>> remove_space("  ho ge fu   ga    ")
    "hogefuga"
    """
    return re.sub("\s|\t", "", s)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
