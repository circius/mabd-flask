# -*- coding: utf-8 -*-
"""encapsulates helper functions for mabd

"""
import os
from typing import Union


def get_env_var(name: str) -> str:
    """ consumes the name of an environment variable and produces its
value.  
"""
    return os.getenv(name)


def get_env_var_checked(name: str) -> str:
    """ consumes the name of an environment variable and produces its value, if
it has a value, or exits with a warning.
"""
    value = os.getenv(name)
    try:
        assert value != None
    except AssertionError:
        print(f"Compulsory environment variable {name} unset: exiting.")
        exit(1)
    return value


def no_nonesP(l: list):
    """ consumes a list and produces True if no element of the list is None, 
False otherwise
"""

    if len(l) is 0:
        return True
    return l[0] is not None and no_nonesP(l[1:])
