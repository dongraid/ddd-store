from domain import events, commands, model
from service_layer import unit_of_work


def create_product(command, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        product = model.Product(name=command.name, price=command.price)
        uow.products.add(product)
        uow.commit()
        product.make_event()


def product_created(event, uow: unit_of_work.AbstractUnitOfWork):
    print('Product created!')
    print(event)


def add_to_read_model(event, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        advise = 'Buy' if event.price > 5 else 'Skip'
        uow.session.execute(
            """
            INSERT INTO products_read (name, price, advise)
            VALUES (:name, :price, :advise)
            """,
            dict(name=event.name, price=event.price, advise=advise),
        )
        uow.commit()


COMMAND_HANDLERS = {
    commands.CreateProduct: create_product
}

EVENT_HANDLERS = {
    events.ProductCreated: [product_created, add_to_read_model]
}
