from adapters import orm
from service_layer.messagebus import MessageBus
from service_layer import handlers
from service_layer import unit_of_work


def start():
    orm.start_mappers()

    bus = MessageBus(
        unit_of_work.SqlAlchemyUnitOfWork(),
        handlers.EVENT_HANDLERS,
        handlers.COMMAND_HANDLERS
    )
    return bus

