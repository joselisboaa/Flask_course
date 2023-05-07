import uuid
from db import items, stores
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}, 200


    def post(self):
        item_data = request.get_json()
        for item in items.values():
            print(item)
            if item["store_id"] == item_data["store_id"] or item["name"] == item_data["name"]:
                abort(400, message="O item já existe.")
        if item_data["store_id"] not in stores:
            abort(404, message="Loja não encontrada.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            return {"message": "Item não encontrado."}, 404

    def put(self, item_id):
        item_data = request.get_json()
        try:
            item = items[item_id]
            item |= item_data
            return item, 201
        except KeyError:
            abort(404, message="Item não encontrado")


    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deletado com sucesso."}, 204
        except KeyError:
            abort(404, message="Item não encontrado.")