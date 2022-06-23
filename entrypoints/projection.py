from service_layer import unit_of_work


def get_products(uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        results = uow.session.execute(
            """
            SELECT * FROM products_read
            """
        )
    return [dict(r) for r in results]
