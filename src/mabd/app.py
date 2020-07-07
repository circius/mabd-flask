from __future__ import annotations

# -*- coding: utf-8 -*-
""" encapsulates functions for parsing and adjusting Airtable objects

"""
import airtable
from typing import Dict, List, Union

from mabd import airtable_interface


class MABD(object):
    def __init__(self, verbose=False):
        self.TABLE_NAMES = [
            "deliveries",
            "requests",
            "offers",
            "drivers",
            "people",
            "statuses",
        ]
        self.TABLES = airtable_interface.get_all_tables(self.TABLE_NAMES)
        self._verbose = verbose

    def update_delivery(self, delivery_id: str, update_dict: dict) -> Delivery:
        """consume a delivery_id and an update_dicts. produce a copy of the
corresponding delivery with all fields corresponding to keys in the
dict updated to the corresponding values; as a side-effect, produce
this effect on the airtable.

        """
        delivery_dict = self.update_record_in_table(
            "deliveries", delivery_id, update_dict
        )
        return Delivery(delivery_dict)

    def update_request(self, request_id: str, update_dict: dict) -> Request:
        """consume a request_id and an update_dicts. produce a copy of the
corresponding delivery with all fields corresponding to keys in the
dict updated to the corresponding values; as a side-effect, produce
this effect on the airtable.

        """
        request_dict = self.update_record_in_table("requests", request_id, update_dict)
        return Request(request_dict)

    def update_record_in_table(
        self, table_name: str, record_id: str, update_dict: dict
    ) -> dict:
        """I consume the name of a table, the id of a record in that table,
and an update_dict, and produce a copy of the corresponding record
with all fields corresponding to keys in the dict updated to the
corresponding values; as a side-effect, I produce this effect on the
airtable.


        """
        airtable = self.get_airtable(table_name)
        return airtable.update(record_id, update_dict, typecast=True)

    def update_offer(self, offer_id: str, update_dict: dict) -> Offer:
        """consume a offer_id and an update_dicts. produce a copy of the
corresponding delivery with all fields corresponding to keys in the
dict updated to the corresponding values; as a side-effect, produce
this effect on the airtable.

        """
        offer_dict = self.update_record_in_table("offers", offer_id, update_dict)
        return Offer(offer_dict)

    def get_unfulfilled_delivery_records(self) -> List[Delivery]:
        """ consumes nothing and gets all unfulfilled deliveries from the airtable.
            """
        delivery_dicts = self.get_airtable("deliveries").get_all(
            view="unfulfilled deliveries"
        )
        return [Delivery(delivery_dict) for delivery_dict in delivery_dicts]

    def get_airtable(self, table_name: str) -> airtable.Airtable:
        """ consume the name of a table and produce the corresponding airtable.
"""
        return self.TABLES[table_name]

    def get_delivery_by_number(self, delivery_number: int) -> Delivery:
        """ consumes a delivery number and produces the corresponding delivery.
"""
        return Delivery(self.get_airtable("deliveries").match("id", delivery_number))

    def get_record_from_table_by_id(
        self, table_name: str, record_id: str
    ) -> Union[Record, None]:
        """consumes a table-name and a record_id and produces the
corresponding Record, or None.

        """
        constructors = {"deliveries": Delivery, "requests": Request, "offers": Offer}
        table = self.get_airtable(table_name)

        record_dict = table.get(record_id)

        if record_dict is None:
            return None

        if table_name in constructors.keys():
            return constructors[table_name](record_dict)
        else:
            return Record(record_dict)

    def get_request_by_id(self, request_id: str) -> Request:
        """consume a request_id and produce the corresponding Request from
the requests table.

        """
        return Request(self.get_airtable("requests").get(request_id))

    def get_offer_by_id(self, offer_id: str) -> Offer:
        """" consume an offer_id and produce the corresponding Offer from the
offers table.

        """
        offer_dict = self.get_airtable("offers").get(offer_id)
        return Offer(offer_dict)

    def delivery_get_minimal_representation(self, delivery: Delivery) -> dict:
        """consumes a Delivery and produces a minimal dict representation of
        it with the keys `id`, `to`, `from`, `driver`, and `date`, with human-readable
        values.
        
        """
        return delivery.get_minimal_representation(self)

    def get_pprinted_delivery(self, delivery: Delivery) -> str:
        """ consumes a delivery_dict and pretty-prints it.
"""
        return delivery.pprint(self)

    def do_delivery_fulfilment(self, delivery_number: int) -> Union[Delivery, bool]:
        """does fulfilment of a delivery specified by its
        number, adjusting all requests and offers associated with that
        delivery. Returns the delivery if the the fulfilment is successful,
        False otherwise.
        
        """
        delivery_dict = self.get_airtable("deliveries").match("id", delivery_number)
        if delivery_dict == {}:
            return False
        delivery = Delivery(delivery_dict)
        after_fulfilment = delivery.do_fulfilment(self)
        return after_fulfilment

    def request_get_minimal_representation(self, record: Record) -> dict:
        """consumes a record and produces a minimal representation of the
record as a dict with readable values.

        """
        return record.get_minimal_representation(self)

    def get_unfulfilled_requests_of_person(self, person_name: str) -> List[Request]:
        """consumes the name of a person in the airtable and produces a list
of that person's unfulfilled requests.

        """
        all_open_requests = self.get_airtable("requests")
        search_formula = f"{{requested_by}}='{person_name}'"
        persons_requests = all_open_requests.get_all(
            formula=search_formula, view="open requests"
        )

        return persons_requests

    def get_readable_unfulfilled_requests_of_person(
        self, person_name: str
    ) -> List[dict]:
        """consumes the name of a person in the airtable and produces a list
of that person's unfulfilled requests, represented as dicts with human-readable values.

        """
        request_dicts = self.get_unfulfilled_requests_of_person(person_name)
        requests = [Request(request_dict) for request_dict in request_dicts]
        return [
            self.request_get_minimal_representation(request) for request in requests
        ]

    def get_readable_matching_offers_for_requestID(self, request_id: str) -> List[dict]:
        """consumes the ID of a request and produces a list of that request's matching offers,
represented as dicts with human-readable values.
"""
        request = self.get_record_from_table_by_id("requests", request_id)
        print(f"getting matching offers for {request} with request_id {request_id}")
        matching_offer_ids = request.get_field("matching_offers")
        print(f"matching offer ids: {matching_offer_ids}")
        matching_offers = [
            self.get_record_from_table_by_id("offers", offer_id)
            for offer_id in matching_offer_ids
        ]
        print(f"matching offers: {matching_offers}")
        return [offer.get_minimal_representation(self) for offer in matching_offers]

    def get_person_by_person_name(self, person_name: str) -> Union[Record, bool]:
        """consumes a person_name and returns the record from the 'people'
table with that name, or False if it's not found.
        """

        person_table = self.get_airtable("people")
        person_dict = person_table.match("name", person_name)

        if person_dict == {}:
            return False

        return Record(person_dict)


class Record(object):
    def __init__(self, record_dict: dict):
        self._record_dict = record_dict
        self._record_id = record_dict["id"]
        self._fields = record_dict["fields"]

    def __getitem__(self, item):
        return self._record_dict[item]

    def get_id(self):
        return self._record_id

    def get_field(self, field_name, default=[]) -> list:
        try:
            return self._fields[field_name]
        except KeyError:
            return default

    def get_columns(self):
        return self._fields.keys()


class Offer(Record):
    def do_fulfilment(self, mabd: MABD) -> Offer:
        """ consume an mabd-state, and produce myself with 
my status set to 'fulfilled'. as a side-effect, produce this 
effect on the airtable.
"""
        fulfilled_offer = self._set_field(mabd, "status", "fulfilled")
        return fulfilled_offer

    def _set_field(self, mabd: MABD, field_name: str, value: any) -> Request:
        """ consume an mabd-state, a field_name and a value, and produce a copy of myself
        with the corresponding field set to that value.

        As a side-effect, produce this effect on the mabd-state.
        """
        return mabd.update_offer(self.get_id(), {field_name: [value]})

    def get_minimal_representation(self, mabd: MABD) -> dict:
        """consume an mabd-state, and produce a readable representation of
myself expressed as a dict.

        """

        donor_records = self.get_records_from_table_for_ids_in_field(
            "donor", "people", mabd
        )

        donor = ", ".join([record.get_field("name") for record in donor_records])

        name = self.get_field("name")

        return {
            "name": name,
            "donor": donor,
        }

    def get_records_from_table_for_ids_in_field(
        self, field_name, table, mabd: MABD
    ) -> List[Record]:
        record_ids = self.get_field(field_name)
        return [
            mabd.get_record_from_table_by_id(table, record_id)
            for record_id in record_ids
        ]


class Request(Record):

    # def record_get_fields(self, record) -> List:
    #     """consumes an airtable Record and produces its fields.
    #     """
    #     return record["fields"]

    def get_confirmed_offerID(self) -> Union[str, None]:
        """ I produce my confirmed offer, if I have one, or raise a KeyError and return None if not.
        """
        result = self.get_field("confirmed_offer")

        if result == []:
            return None
        else:
            return result.pop()

    def get_matching_offerIDs(self) -> list:
        """ I produce the list of my matching offers.
        """
        return self.get_field("matching_offers")

    def do_fulfilment(self, mabd: MABD) -> Request:
        """ consume an mabd-state, and produce myself with 
          1. my status set to 'fulfilled'.
          2. with all of my "matching offers" removed
        as a side-effect, produce this effect on the airtable.
        also:
          3. set the status of all of my "confirmed offers" to "fulfilled".
"""
        fulfilled_request = self._set_field(mabd, "status", "fulfilled")
        without_matches = fulfilled_request._set_field(mabd, "matching_offers", [])

        confirmed_offerID = self.get_confirmed_offerID()
        confirmed_offer = mabd.get_offer_by_id(confirmed_offerID)
        confirmed_offer_fulfilled = confirmed_offer.do_fulfilment(mabd)

        return without_matches

    def _set_field(self, mabd: MABD, field_name: str, value: any) -> Request:
        """ consume an mabd-state, a field_name and a value, and produce a copy of myself
        with the corresponding field set to that value.

        As a side-effect, produce this effect on the mabd-state.
        """
        updated_request = mabd.update_request(self.get_id(), {field_name: value})
        return Request(updated_request)

    def get_minimal_representation(self, mabd: MABD) -> dict:
        """consume an mabd-state, and produce a readable representation of
myself expressed as a dict.

        """

        requested_by_records = self.get_records_from_table_for_ids_in_field(
            "requested_by", "people", mabd
        )

        requested_by = ",".join(
            [record.get_field("name") for record in requested_by_records]
        )

        item = self.get_field("item")

        return {
            "item": item,
            "requested_by": requested_by,
        }

    def get_records_from_table_for_ids_in_field(
        self, field_name, table, mabd: MABD
    ) -> List[Record]:
        record_ids = self.get_field(field_name)
        return [
            mabd.get_record_from_table_by_id(table, record_id)
            for record_id in record_ids
        ]


class Delivery(Record):
    def __str__(self):
        return f"""Delivery with:
  - record_id: {self._record_id}
  - number: {self.get_delivery_number()} and 
  - fulfilled?: {self.get_fulfilment()}.
"""

    def _set_field(self, mabd: MABD, field_name: str, value: any) -> Delivery:
        """consume an mabd-state, a field_name and a value, and produce a
        copy of myself with the corresponding field set to that
        value. as a side-effect, produce this effect on the mabd-state.

        """
        updated_delivery = mabd.update_delivery(self.get_id(), {field_name: value})
        return Delivery(updated_delivery)

    def get_fulfilment(self) -> bool:
        return self.get_field("fulfilled?", False)

    def get_delivery_number(self) -> int:
        return self.get_field("id", -1)

    def do_fulfilment(self, mabd: MABD) -> Delivery:
        """consume an mabd-state, and produce a copy of myself with my 'fulfilment' status set to 'true'.
as a side-effect, produce this effect on the airtable.
        also:
        1. set the status of all requests associated with the delivery to 'fulfilled'
        2. set the status of all "confirmed offers" for those requests to 'fulfilled'.
        3. remove all 'matching offers' from those requests.

        """
        request_ids = self.get_field("requests")
        requests_fulfilled = [mabd.get_request_by_id(r_id) for r_id in request_ids]
        for request in requests_fulfilled:
            request.do_fulfilment(mabd)

        fulfilled_delivery = self._set_field(mabd, "fulfilled?", True)
        return fulfilled_delivery

    def get_all_requestIDs(self) -> list:
        """ I produce a list of all the requests fulfilled by me.
            """

        return self.get_field("requests")

    def pprint(self, mabd: MABD) -> str:
        """ produce a readable representation of myself, based on the 
        contents of other tables in the MABD.
        """
        readable_delivery = self.get_minimal_representation(mabd)
        delivery_id, to, frm, driver, date = readable_delivery.values()
        return f"""Delivery {delivery_id}:
        - to: {to}
        - from: {frm}
        - driver: {driver}
        - date: {date}
        """

    def get_records_from_table_for_ids_in_field(
        self, field_name, table, mabd: MABD
    ) -> List[Record]:
        record_ids = self.get_field(field_name)
        return [
            mabd.get_record_from_table_by_id(table, record_id)
            for record_id in record_ids
        ]

    def get_minimal_representation(self, mabd: MABD):
        delivery_number = self.get_field("id")

        to_records = self.get_records_from_table_for_ids_in_field("to", "people", mabd)
        to = ", ".join([record.get_field("name") for record in to_records])

        frm_records = self.get_records_from_table_for_ids_in_field(
            "from", "people", mabd
        )
        frm = ", ".join([record.get_field("name") for record in frm_records])

        driver_records = self.get_records_from_table_for_ids_in_field(
            "driver", "drivers", mabd
        )
        driver = ", ".join([record.get_field("name") for record in driver_records])

        date = self.get_field("date")

        return {
            "delivery_number": delivery_number,
            "to": to,
            "from": frm,
            "driver": driver,
            "date": date,
        }


if __name__ == "__main__":
    import sys

    interface = MABD()
    if len(sys.argv) == 1:
        unfulfilled = interface.get_unfulfilled_delivery_records()
        readable_unfulfilled = [
            interface.get_pprinted_delivery(delivery) for delivery in unfulfilled
        ]
        for delivery in readable_unfulfilled:
            print(delivery)
        exit(0)
    delivery_number = sys.argv[1]
    print(f"fulfilling delivery with number {delivery_number}")
    result = interface.do_delivery_fulfilment(delivery_number)
    print(f"result: {result}")
