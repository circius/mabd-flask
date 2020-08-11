# -*- coding: utf-8 -*-
""" encapsulates functions for getting airtable data

"""
import os
from typing import List, Dict

from airtable import Airtable

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE = os.getenv("BASE_ID")

def get_all_tables(table_names) -> Dict[str, Airtable]:
    return {x: Airtable(BASE, x) for x in table_names}
