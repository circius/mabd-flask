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

    def get_unfulfilled_delivery_records(self) -> List:
        """ consumes nothing and gets all unfulfilled deliveries from the airtable.
            """
        return self.TABLES["deliveries"].get_all(view="unfulfilled deliveries")

    def delivery_get_all_requestIDs(self, delivery) -> Union[List[str], None]:
        """consumes a delivery Record and produces a list of the IDs of the requests
            fulfilled by it, or None.
        """
        try:
            result = self.record_get_fields(delivery)["requests"]
        except ValueError:
            if verbose:
                print(f"No requests found for delivery:\n {delivery}")
                return None
        return result

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


def table_names_get_all_data(table_names: List[str]) -> Dict[str, dict]:
    """consumes a list of names of tables within an airtable base and
produces a Dict whose keys are the names and whose values are the tables.

    """
    airtables = airtable_interface.get_all_tables(table_names)
    # print(f"got airtables: {airtables} from base {airtable_interface.BASE}")
    return {key: airtables[key].get_all() for key in airtables.keys()}


def do_delivery_fulfilment(delivery_number: int) -> bool:
    """imperative function. does fulfilment of a delivery specified by its
number, adjusting all requests and offers associated with that
delivery.

    """
    delivery_record = TABLES["deliveries"].match(
        "id", delivery_number, view="unfulfilled deliveries"
    )
    try:
        deliveryID = delivery_record["id"]
    except KeyError:
        return False
    return deliveryID_do_recursive_fulfilment(deliveryID)


def deliveryID_do_recursive_fulfilment(deliveryID: str) -> bool:
    """imperative function. does fulfilment of a delivery, adjusting all
requests and offers associated with that delivery.

    """
    # print("marking delivery fulfilled")
    fulfilled_delivery = deliveryID_fulfil_delivery(deliveryID)

    # also fulfils confirmed offers
    # print("processing fulfilled requests")
    requestIDs = deliveryID_get_all_recordIDs(deliveryID)
    fulfilled_requests = requestIDs_do_recursive_fulfilment(requestIDs)

    return True


def deliveryID_get_all_recordIDs(deliveryID: str) -> List:
    """consumes a deliveryID and produces all the corresponding recordIDs.
    """
    delivery = TABLES["deliveries"].get(deliveryID)
    return delivery_get_all_requestIDs(delivery)


def deliveryID_fulfil_delivery(deliveryID: str) -> List:
    """ consumes a deliveryID and fulfils it on the airtable.
"""
    return TABLES["deliveries"].update(deliveryID, {"fulfilled?": True}, typecast=True)


def deliveryID_get_delivery(deliveryID: str) -> List:
    """consumes the id of a row of the Deliveries table and produces the
corresponding record.

    """
    return TABLES["deliveries"].get(deliveryID)


def deliveryID_mark_requests_fulfilled(deliveryID: str) -> List:
    """consumes a deliveryID and produces a list of the corresponding
requests, their statuses all changed to "fulfilled." As a side-effect,
performs the corresponding change on the airtable.

    """
    delivery = deliveryID_get_delivery(deliveryID)
    requestIDs = delivery_get_all_requestIDs(delivery)
    return requestIDs_do_recursive_fulfilment(requestIDs)


def requestIDs_do_recursive_fulfilment(requestIDs: list) -> List:
    """consumes a [List-of requestIDs] and produces a [List=-of requests]
in which:
    1) the status of the request has been set to "fulfilled"
    2) all the request's matching offers have been removed;
as a side-effect, it also does this to the corresponding airtable records, and
marks the confirmed offer of each record as 'fulfilled'.
"""
    # side-effects
    # print(f"marking confirmed offers fulfilled")
    fulfilled_offers = requestIDs_fulfil_confirmed_offerIDs(requestIDs)
    # print(f"all fulfilled offers: {fulfilled_offers}")
    # proper function
    # print(f"marking requests fulfilled")
    fulfilled_requests = requestIDs_mark_requests_fulfilled(requestIDs)
    # print(f"and stripping them of matches")
    without_matches = requestIDs_remove_matching_offers(requestIDs)
    # print(f"resulting fulfilled requests::\n {without_matches}")
    return without_matches


def requestIDs_get_confirmed_offerIDs(requestIDs: list) -> List[str]:
    """consumes a list of requestIDs and produces a list pf the
corresponding confirmed offerIDs.

    """
    return [requestID_get_confirmed_offerID(requestID) for requestID in requestIDs]


def offerIDs_fulfil_offer(offerIDs: list) -> List:
    """consumes a [List-of offerIDs] and produces a corresponding [List-of
offers] in which the status of every offer has been forced to
'fulfilled'. as a side-effect, produces the same effect in the
airtable.

    """
    return [offerID_mark_status_fulfilled(offerID) for offerID in offerIDs]


def requestIDs_fulfil_confirmed_offerIDs(requestIDs: list) -> List:
    """consumes a [List-of requestIDs] and produces a [List-of Offers]
corresponding to the offers fulfilled by the fulfilment of those
requests, with their statuses forced to 'fulfilled'. As a side-effect,
produces this effect on the airtable.

    """
    offerIDs = [requestID_get_confirmed_offerID(requestID) for requestID in requestIDs]
    return [offerID_mark_status_fulfilled(offerID) for offerID in offerIDs]


def offerID_mark_status_fulfilled(offerID: str) -> List:
    """consumes an offerID and produces an offer with the status forced to
"fulfilled". As a side-effect, produces the same effect on the
airtable.

    """
    return TABLES["offers"].update(offerID, {"status": "fulfilled"}, typecast=True)


def requestID_get_confirmed_offerID(requestID: str) -> Union[str, None]:
    """ consumes a requestID and gets the corresponding offerID, or None if the offerID isn't set.
"""
    request = TABLES["requests"].get(requestID)
    return request_get_confirmed_offerID(request)


def requestIDs_remove_matching_offers(requestIDs: list) -> List:
    """consumes a list of requestIDs and produces the corresponding
[List-of requests], with no entries in the 'matching_offers'
column. As a side-effect, it also updates the airtable accordingly.

    """
    return [requestID_remove_matching_offers(requestID) for requestID in requestIDs]


def requestID_remove_matching_offers(requestID: str) -> List:
    """consumes a requestID and produces the corresponding request, with
no entries in the 'matching_offers' column. As a side-effect, it also
updates the airtable accordingly.

    """
    return [
        TABLES["requests"].update(requestID, {"matching_offers": None}, typecast=True)
    ]


def requestIDs_mark_requests_fulfilled(requestIDs: list) -> List:
    """consumes a [List-of requestIDs] and returns the corresponding
[List-of requests] with the status forced to 'fulfilled.' As a side
effect, it also updates the airtable accordingly.

    """

    return [requestID_mark_request_fulfilled(requestID) for requestID in requestIDs]


def requestID_mark_request_fulfilled(requestID: str) -> List:
    """consumes a requestID and returns the corresponding request with
the status forced to 'fulfilled.' As a side effect, it also updates
the airtable accordingly.

    """
    return [
        TABLES["requests"].update(requestID, {"status": "fulfilled"}, typecast=True)
    ]


def request_get_minimal_representation(request: list) -> dict:
    """consumes a request and produces a minimal dict representation of it
with the keys `id` `item` `requested_by` and `status` and with
human-readable values.

    """
    try:
        request_id = request["id"]
    except:
        request_id = "couldn't get id"
        print(f"Couldn't get id for request {request_record}, something is very wrong")
    fields = request["fields"]
    try:
        item = fields["item"]
    except:
        item = "Couldn't get item"
    try:
        requested_by_record = TABLES["people"].get(fields["requested_by"][0])
        requested_by = requested_by_record["fields"]["name"]
    except:
        requested_by = "Couldn't get name of requester"
    try:
        status_record = TABLES["statuses"].get(fields["status"][0])
        status = status_record["fields"]["name"]
    except:
        status = "couldn't get status"

    return {
        "id": request_id,
        "item": item,
        "requested_by": requested_by,
        "status": status,
    }


def delivery_get_minimal_representation(delivery) -> dict:
    """consumes a delivery and produces a minimal dict representation of
it with the keys `id`, `to`, `from`, `driver`, and `date`, with human-readable
values.

    """
    try:
        record_id = delivery["id"]
    except:
        record_id = "couldn't get id"
        print(f"Couldn't get id for delivery {delivery}, something is very wrong.")
    fields = record_get_fields(delivery)
    delivery_id = fields["id"]
    try:
        to_record = TABLES["people"].get(fields["to"][0])
        to = to_record["fields"]["name"]
    except:
        to = "couldn't fetch to"
    try:
        frm_record = TABLES["people"].get(fields["from"][0])
        frm = frm_record["fields"]["name"]
    except:
        frm = "couldn't fetch from"
    try:
        driver_record = TABLES["drivers"].get(fields["driver"][0])
        driver = driver_record["fields"]["name"]
    except:
        driver = "couldn't fetch driver."
    try:
        date = fields["date"]
    except:
        date = "couldn't fetch date"

    return {
        "delivery_id": delivery_id,
        "to": to,
        "from": frm,
        "driver": driver,
        "date": date,
    }


## pretty printing
def format_request(request: List) -> str:
    """ consumes a request and produces a readable representation of it.
"""
    readable_request = request_get_minimal_representation(request)
    request_id, item, requested_by, status = readable_request.values()
    return f"""Request {request_id}:
    item: {item}
    requested_by: {requested_by}
    status: {status}
"""


def format_delivery(delivery) -> str:
    """ consumes a delivery and produces a readable representation of it.
"""
    readable_delivery = delivery_get_minimal_representation(delivery)
    delivery_id, to, frm, driver, date = readable_delivery.values()
    return f"""Delivery {delivery_id}:
    - to: {to}
    - from: {frm}
    - driver: {driver}
    - date: {date}
"""


if __name__ == "__main__":
    import sys

    deliveryID = sys.argv[1]
    print(f"fulfilling delivery {deliveryID}")
    result = deliveryID_do_recursive_fulfilment(deliveryID)
    print(f"result: {result}")
