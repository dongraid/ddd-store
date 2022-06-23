from domain import events


class Product:
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price
        self.events = []

    def make_event(self):
        self.events.append(
            events.ProductCreated(
                name=self.name,
                price=self.price
            )
        )
