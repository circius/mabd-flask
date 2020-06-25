# -*- coding: utf-8 -*-
""" encapsulates functions for parsing and adjusting Airtable objects

"""
import airtable
from typing import Dict, List, Union

from mabd import airtable_interface

TABLE_NAMES = ["deliveries", "requests", "offers", "drivers", "people", "statuses"]

TABLES = airtable_interface.get_all_tables(TABLE_NAMES)


def table_names_get_all_data(table_names: List[str]) -> Dict[str, dict]:
    """consumes a list of names of tables within an airtable base and
produces a Dict whose keys are the names and whose values are the tables.

    """
    airtables = airtable_interface.get_all_tables(table_names)
    # print(f"got airtables: {airtables} from base {airtable_interface.BASE}")
    return {key: airtables[key].get_all() for key in airtables.keys()}


def delivery_get_all_requestIDs(delivery) -> Union[List[str], None]:
    """consumes a delivery Record and produces a list of the IDs of the requests
fulfilled by it, or None.
"""
    try:
        result = record_get_fields(delivery)["requests"]
    except ValueError:
        # print(f"No requests found for delivery:\n {delivery}")
        return None
    return result


def record_get_fields(record) -> List:
    """consumes an airtable Record and produces its fields.
"""
    return record["fields"]


def request_get_confirmed_offerID(request) -> Union[str, None]:
    """ consumes a request Record and produces the ID of its confirmed offer, if it
has one, or None otherwise.
"""
    try:
        result = record_get_fields(request)["confirmed_offer"][0]
    except KeyError:
        print(
            f"No confirmed offer found for request:\n {format_request(request)}. \n Aborting."
        )
        exit(1)
    return result


def request_get_matching_offerIDs(request) -> list:
    """ consumes a request record and produces the IDs of its matching offers.
"""
    try:
        result = record_get_fields(request)["matching_offers"]
    except KeyError:
        print(f"No matching offers found for request:\n {format_request(request)}")
        return []
    return result


