from entrypoints import projection
from flask import Flask, jsonify
import bootstrap
from domain import commands

app = Flask(__name__)
bus = bootstrap.start()


@app.route("/products", methods=["POST"])
def create_products():
    command = commands.CreateProduct(name='Test2', price=20)
    bus.handle(command)
    return "OK", 201


@app.route("/products", methods=["GET"])
def get_products():
    response = projection.get_products(bus.uow)
    return jsonify(response)
