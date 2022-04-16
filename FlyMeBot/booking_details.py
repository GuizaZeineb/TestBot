# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class BookingDetails:
    def __init__(
        self,
        destination: str = None,
        origin: str = None,
 #       travel_date: str = None,
        departure_date: str = None,
        arrival_date: str = None,
        budget: str = None ,
        number: int = None,
        units :str = None,
        unsupported_airports=None,
    ):
        #if unsupported_airports is None:
        #    unsupported_airports = []
        self.destination = destination
        self.origin = origin
        self.unsupported_airports = unsupported_airports
#        self.travel_date = travel_date
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.budget = budget,
        self.number = number,
        self.units  = units