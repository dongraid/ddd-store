from dataclasses import dataclass


class Event:
    pass


@dataclass
class ProductCreated(Event):
    name: str
    price: int
