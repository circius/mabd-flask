from typing import List

from mabd import app


def get_readable_unfulfilled_deliveries() -> List[dict]:
    """consumes nothing and produces a list of all the unfulfilled
deliveries, represented as a minimal dict with the keys `id`, `to`,
`from`, `driver`, and `date`.

    """
    unfulfilled_deliveries = app.get_unfulfilled_delivery_records()
    minimal_representations = [
        app.delivery_get_minimal_representation(delivery)
        for delivery in unfulfilled_deliveries
    ]
    return minimal_representations


def get_pretty_unfulfilled_deliveries() -> List[str]:
    """consumes nothing and produces a list of all the unfulfilled
deliveries, represented as strings.

    """
    deliveries = app.get_unfulfilled_delivery_records()
    print([delivery for delivery in deliveries])
    return [app.format_delivery(delivery) for delivery in deliveries]


def do_delivery_fulfilment(delivery_id: str) -> bool:
    """consumes the value of the delivery_id column of a delivery and
produces True if if this succeedsm false otherwise. As a side-effect, processes
all of the requests and offers associated with the delivery.

    """

    return app.do_delivery_fulfilment(delivery_id)
