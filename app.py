from flask import Flask, request
from db import items, stores
from flask_smorest import abort
import uuid

app = Flask(__name__)

city = [
    {
        "name": "Fortaleza"
    }
]


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="name é obrigatório")

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="A Loja já existe.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/store/<string:store_id>/item")
def create_item():
    try:
        item_data = request.get_json()
        if item_data["store_id"] not in stores:
            return {"message": "Loja não encontrada"}, 404
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        item_data[item_id] = item
        return item, 201
    except KeyError:
        abort(400, message="Não foi possível criar o item")


@app.post("/item")
def create_item():
    item_data = request.get_json()

    if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
        abort(400, message="É necessário um price, store_id e name.")
    for item in items.values():
        if item["store_id"] == item_data["store_id"] or item["name"] == item_data["name"]:
            abort(400, message="O item já existe.")
    if item_data["store_id"] not in stores:
        abort(404, message="Loja não encontrada.")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.post("/machine")
def create_machine():
    try:
        request_data = request.get_json()
        new_machine = {
            "name": request_data["name"], "abbreviation": request_data["abbreviation"],
            "space_id": request_data["space_id"], "patrimony": request_data["patrimony"]
        }
        return new_machine, 201
    except:
        abort(400, "Erro ao criar máquina.")

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        abort(404, message="Loja não encontrada")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        return {"message": "Item não encontrado."}, 404

@app.get("/city")
def get_city():
    return {"city": city}
