# -*- coding: utf-8 -*-
""" encapsulates functions for getting airtable data

"""
from typing import List, Dict
from airtable import Airtable

from mabd import utilities

AIRTABLE_API_KEY = utilities.get_env_var_checked("AIRTABLE_API_KEY")
BASE = utilities.get_env_var_checked("BASE_ID")


def get_all_tables(table_names) -> Dict[str, Airtable]:
    return {x: Airtable(BASE, x) for x in table_names}
