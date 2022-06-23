from typing import Union
import logging
from service_layer.unit_of_work import AbstractUnitOfWork
from domain.events import Event
from domain.commands import Command

logger = logging.getLogger(__name__)
Message = Union[Event, Command]


class MessageBus:
    def __init__(self, uow: AbstractUnitOfWork, event_handler, command_handler):
        self.uow = uow
        self.event_handler = event_handler
        self.command_handler = command_handler

    def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Event):
                self.handle_event(message)
            elif isinstance(message, Command):
                self.handle_command(message)
            else:
                raise NotImplemented

    def handle_event(self, event):
        for handler in self.event_handler[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event, self.uow)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception("Exception handling event %s", event)
                raise

    def handle_command(self, command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handler[type(command)]
            handler(command, self.uow)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise
