import logging
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    event,
)
from sqlalchemy.orm import mapper
from domain import model

logger = logging.getLogger(__name__)

metadata = MetaData()

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("price", Integer),
)


def start_mappers():
    logger.info("Starting mappers")
    mapper(model.Product, products)


@event.listens_for(model.Product, "load")
def receive_load(product, _):
    product.events = []
