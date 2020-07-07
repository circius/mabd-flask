from typing import List, Union

from mabd.app import MABD, Delivery, Request


def get_readable_unfulfilled_deliveries() -> List[dict]:
    """consumes nothing and produces a list of all the unfulfilled
deliveries, represented as a minimal dict with the keys `id`, `to`,
`from`, `driver`, and `date`.

    """
    interface = MABD()
    unfulfilled_deliveries = interface.get_unfulfilled_delivery_records()
    minimal_representations = [
        interface.delivery_get_minimal_representation(delivery)
        for delivery in unfulfilled_deliveries
    ]
    return minimal_representations


def get_pretty_unfulfilled_deliveries() -> List[str]:
    """consumes nothing and produces a list of all the unfulfilled
deliveries, represented as strings.

    """
    interface = MABD()
    deliveries = interface.get_unfulfilled_delivery_records()
    return [interface.get_pprinted_delivery(delivery) for delivery in deliveries]


def do_delivery_fulfilment(delivery_id: str) -> Union[Delivery, bool]:
    """consumes the value of the delivery_id column of a delivery and
produces the Delivery if this succeeds, and False otherwise. As a side-effect, processes
all of the requests and offers associated with the delivery.

    """
    interface = MABD()
    return interface.do_delivery_fulfilment(delivery_id)


def get_readable_unfulfilled_requests_of_person(person_name: str) -> List[dict]:
    """consumes the name of a person and returns the list of all of that
person's requests, represented as dicts with readable values.

    """
    interface = MABD()
    return interface.get_readable_unfulfilled_requests_of_person(person_name)


def get_name_of_requested_item_from_requestID(requestID: str) -> str:
    """consumes a requestID and produces the name of the corresponding
request.

    """
    interface = MABD()
    request = interface.get_record_from_table_by_id("requests", requestID)
    item_name = request.get_field("item")
    return item_name


def get_readable_matching_offers_for_requestID(request_id: str) -> List[dict]:
    """consumes the id of an open request and produces the list of all of
the corresponding request's matching offers, represented as dicts with
readable values.

    """
    interface = MABD()
    return interface.get_readable_matching_offers_for_requestID(request_id)


def get_readable_offer_by_offer_number(offer_number: int) -> dict:
    """ consumes an offer-number and produces the corresponding offer, 
represented as a readable dict.
"""
    interface = MABD()
    return interface.get_readable_offer_by_offer_number(offer_number)
