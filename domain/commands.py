from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateProduct(Command):
    name: str
    price: int
