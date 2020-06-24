# -*- coding: utf-8 -*-
""" encapsulates functions for getting airtable data

"""
from typing import List, Dict
import airtable

from mabd import utilities

AIRTABLE_API_KEY = utilities.get_env_var("AIRTABLE_API_KEY")
BASE_ID = utilities.get_env_var("BASE_ID")

TABLE_NAMES = ["deliveries", "requests", "offers", "drivers", "people", "statuses"]


def get_all_tables(table_names: List[str]) -> Dict[str, airtable.Airtable]:
    return {x: lambda x: airtable.Airtable(BASE_ID, x) for x in TABLE_NAMES}
