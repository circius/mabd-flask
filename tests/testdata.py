from __future__ import annotations

import json
import os
from typing import List


class TestData(object):

    TESTDATA_PATH = "./tests/testdata_from_matching.json"

    def __init__(self):
        self.data = self._get_raw_testdata()

    def __getitem__(self, item):
        return self.get_table(item)

    def keys(self):
        return self.get_table_names()

    # private methods

    def _get_raw_testdata(self) -> dict:
        """consumes nothing and produces the testdata as a dict.

        """
        with open(self.TESTDATA_PATH, "r") as json_file:
            return json.load(json_file)

    # public methods

    def get_table_names(self) -> List[str]:
        """produces the list of the testdata's tables.

        """
        return self.data.keys()

    def get_table(self, table: str) -> dict:
        """ consumes the name of a table and produces its contents.
        """
        return TestTable(self.data[table])


class TestTable(object):
    def __init__(self, table_dict):
        self.table_dict = table_dict
        self.FULFILLED = "recVpVbXctm0qsL0d"

    def _get_all_over_subset(self, records: List[Record], formula=None):
        """consumes a list of records and does get_all over it. Can handle
formula naively - i.e. only a subset of commands, ad-hoc.  TODO:
should replace this ad-hoc implementation with a proper recursive one
that can handle multiple filters, formulas and so on.

        """
        if formula is not None:
            if "=" in formula:
                # hack to make things work for requests filtered by requested_by
                # will not work if there is more than one operation in the formula
                [lhs_with_braces, rhs_with_quotes] = formula.split("=")
                rhs = rhs_with_quotes.strip("'")
                if "requested_by" in lhs_with_braces:
                    return self._filter_over_field_requested_by(records, rhs)
                raise ValueError(f"Did not recognise formula {formula} with lhs {lhs}")

        return records

    def _filter_over_field_requested_by(
        self, requests: List[TestRecord], person_name: str
    ) -> List[Record]:
        """consumes the name of a Person and a list of requests represented by
TestRecords and produces the subset of the list for which the value of
requested_by is that name.

        """
        result = []
        for request in requests:
            requester_id = request.get_record_field("requested_by")[0]
            person_record_of_requester = (
                TestData().get_table("people").get(requester_id)
            )
            requested_name = person_record_of_requester.get_record_field("name")
            if requested_name == person_name:
                result.append(request)
        return result

    def _get_all_handle_view(self, view, formula=None) -> List[TestRecord]:
        """consumes the name of a view and returns the subset of my records
that match that view. An unrecognised view will not error, but will
produce an empty list.

        """
        records = [TestRecord(record_dict) for record_dict in self.table_dict]

        if view == "unfulfilled deliveries":
            subset = [
                record
                for record in records
                if record.get_record_field("fulfilled?") == []
            ]
            return self._get_all_over_subset(subset, formula)

        elif view == "open requests":
            subset = [
                record
                for record in records
                if record.get_field("status") != [self.FULFILLED]
            ]
            return self._get_all_over_subset(subset, formula)

        return []

    def get_all(self, view=None, formula=None) -> List[TestRecord]:
        """consumes nothing and produces a list of all TestRecords.

        """
        records = [TestRecord(record_dict) for record_dict in self.table_dict]

        if view is not None:
            return self._get_all_handle_view(view, formula)

        return records

    def get(self, record_id) -> Union[TestRecord, None]:
        """consumes nothing and produces the record with id record_id, 
or None if no such record is found.
"""
        records = self.get_all()
        for record in records:
            if record.get_record_id() == record_id:
                return record
        return None

    def match(self, field_name, value) -> Union[TestRecord, dict]:
        """consumes nothing and produces thetox first record with field_name
equal to value, or an empty Dict.

        """
        records = self.get_all()
        for record in records:
            if record.get_record_field(field_name) == value:
                return record
        return {}

    def update(self, record_id, update_dict, **kwargs):
        """consumes a record_id and an update_dict and returns the
corresponding record with each field corresponding to a key in the
dict updated to the corresponding value.

        as a side-effect, produces the same effect in the record
        stored in the table.

        """
        NOTHING = [None, False, []]
        record = self.get(record_id)
        for key in update_dict.keys():
            value = update_dict[key]
            record = record.set_field(key, value)
        return record


class TestRecord(object):
    def __init__(self, record_dict):
        self.record_dict = record_dict

    def __getitem__(self, item):
        return self.record_dict[item]

    def get_record_id(self) -> str:
        """ consumes nothing and produces the id of the record.
"""
        return self.record_dict["id"]

    def get_record_fields(self) -> List:
        """ consumes nothing and gets the fields of the record.
"""
        return self.record_dict["fields"]

    def get_record_field(self, field_name) -> Any:
        """consumes nothing and gets the value of the field with field_name,
or [] if the field doesn't exist

        """
        try:
            result = self.get_field(field_name)
        except KeyError:
            return []
        return result

    def get_fields(self) -> dict:
        return self.record_dict["fields"]

    def get_field(self, field_name):
        return self.record_dict["fields"][field_name]

    def set_field(self, field_name, value) -> dict:
        NOTHING = [None, False, []]
        if value in NOTHING:
            del self.record_dict["fields"][field_name]
        else:
            self.record_dict["fields"][field_name] = value
        return self.record_dict
