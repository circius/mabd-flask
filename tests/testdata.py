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

    def get_all(self, view=None) -> List[TestRecord]:
        """consumes nothing and produces a list of all TestRecords.

        """
        return [TestRecord(record_dict) for record_dict in self.table_dict]

    def get(self, record_id) -> Union[TestRecord, None]:
        """consumes nothing and produces the record with id record_id, 
or None if no suc record is found.
"""
        records = self.get_all()
        for record in records:
            if record.get_record_id() == record_id:
                return record
        return None

    def match(self, field_name, value) -> Union[TestRecord, None]:
        """consumes nothing and produces thetox first record with field_name
equal to value, or None.

        """
        records = self.get_all()
        for record in records:
            if record.get_record_field(field_name) is value:
                return record
        return None

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
        """consumes nothing and gets the value of the field with field_name

        """
        return self.record_dict["fields"][field_name]

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
