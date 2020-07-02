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

    #     self.FULFILLED = self.TABLES['statuses'].match('name', 'fulfilled')['id']

    # def get_fulfilled_id(self):
    #     return self.FULFILLED

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

    def delivery_get_all_requestIDs(self, delivery) -> list:
        """consumes a delivery Record and produces a list of the IDs of the requests
            fulfilled by it.
        """
        delivery_fields = self.record_get_fields(delivery)
        try:
            result = delivery_fields["requests"]
        except KeyError as e:
            return []
        return result

    def get_airtable(self, table_name: str) -> airtable.Airtable:
        """ consume the name of a table and produce the corresponding airtable.
"""
        return self.TABLES[table_name]

    def get_delivery_by_number(self, delivery_number: int) -> Delivery:
        """ consumes a delivery number and produces the corresponding delivery.
"""
        return Delivery(self.get_airtable("deliveries").match("id", delivery_number))

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
        # print(self.get_airtable("offers").get_all())
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

    def record_get_fields(self, record) -> List:
        """consumes an airtable Record and produces its fields.
        """
        return record["fields"]

    def request_get_confirmed_offerID(self, request) -> Union[str, None]:
        """ consumes a request Record and produces the ID of its confirmed offer, if it
    has one, or None otherwise.
        """
        try:
            result = self.record_get_fields(request)["confirmed_offer"][0]
        except KeyError:
            raise KeyError(
                f"No confirmed offer found for request:\n {format_request(request)}. \n Aborting."
            )
        return result

    def request_get_matching_offerIDs(self, request) -> list:
        """ consumes a request record and produces the IDs of its matching offers.
        """
        try:
            result = self.record_get_fields(request)["matching_offers"]
        except KeyError:
            print(f"No matching offers found for request:\n {format_request(request)}")
            return []
        return result

    def do_delivery_fulfilment(self, delivery_number: int) -> bool:
        """does fulfilment of a delivery specified by its
        number, adjusting all requests and offers associated with that
        delivery.
        
        """
        delivery_dict = self.get_airtable("deliveries").match("id", delivery_number)
        delivery = Delivery(delivery_dict)
        return delivery.do_fulfilment(self)


class Record(object):
    def __init__(self, record_dict: dict):
        self._record_dict = record_dict
        self._record_id = record_dict["id"]
        self._fields = record_dict["fields"]

    def __getitem__(self, item):
        return self.get_field(item)

    def get_id(self):
        return self._record_id

    def get_field(self, field_name, default=None):
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


class Request(Record):
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

        try:
            confirmed_offerID = self.get_field("confirmed_offer")[0]
            confirmed_offer = mabd.get_offer_by_id(confirmed_offerID)
            confirmed_offer_fulfilled = confirmed_offer.do_fulfilment(mabd)
        except KeyError as e:
            print(f"{e}\n Request {self.get_id()} has no confirmed offers.")

        return without_matches

    def _set_field(self, mabd: MABD, field_name: str, value: any) -> Request:
        """ consume an mabd-state, a field_name and a value, and produce a copy of myself
        with the corresponding field set to that value.

        As a side-effect, produce this effect on the mabd-state.
        """
        updated_request = mabd.update_request(self.get_id(), {field_name: value})
        return updated_request


class Delivery(Record):
    def __str__(self):
        return f"""Delivery with:
  - record_id: {self._record_id}
  - number: {self.get_delivery_number()} and 
  - fulfilment: {self.get_fulfilment()}.
"""

    def get_fulfilment(self) -> bool:
        return self.get_field("fulfilled?", False)

    def get_delivery_number(self) -> int:
        return self.get_field("id", -1)

    def do_fulfilment(self, mabd: MABD) -> Delivery:
        """consume an mabd-state, and produce myself with my 'fulfilment' status set to 'true'.
as a side-effect, produce this effect on the airtable.
        also:
        1. set the status of all requests associated with the delivery to 'fulfilled'
        2. set the status of all "confirmed offers" for those requests to 'fulfilled'.
        3. remove all 'matching offers' from those requests.

        """
        self._set_field(mabd, "fulfilled?", True)
        request_ids = self.get_field("requests")
        requests_fulfilled = [mabd.get_request_by_id(r_id) for r_id in request_ids]
        for request in requests_fulfilled:
            request.do_fulfilment(mabd)
        return self

    def _set_field(self, mabd: MABD, field_name: str, value: any) -> Delivery:
        """consume an mabd-state, a field_name and a value, and produce a
        copy of myself with the corresponding field set to that
        value. as a side-effect, produce this effect on the mabd-state.

        """
        return mabd.update_record_in_table(
            "deliveries", self.get_id(), {field_name: value}
        )

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

    def get_minimal_representation(self, mabd: MABD):
        people_airtable = mabd.get_airtable("people")
        drivers_airtable = mabd.get_airtable("drivers")

        delivery_number = self.get_field("id")
        try:
            to_record = Record(people_airtable.get(self.get_field("to")[0]))
            to = to_record.get_field("name")
        except:
            to = "couldn't fetch to"
        try:
            frm_record = Record(people_airtable.get(self.get_field("from")[0]))
            frm = frm_record.get_field("name")
        except:
            frm = "couldn't fetch from"
        try:
            driver_record = Record(drivers_airtable.get(self.get_field("driver")[0]))
            driver = driver_record.get_field("name")
        except:
            driver = "couldn't fetch driver"
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
