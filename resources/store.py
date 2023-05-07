import uuid
from db import stores
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def getById(self, store_id):
        try:
            return stores[store_id], 200
        except KeyError:
            abort(404, message="Loja não encontrada")

    def put(self, store_id):
        store_data = request.get_json()

        try:
            store = stores[store_id]
            store |= store_data
            return store, 201
        except KeyError:
            abort(404, message="Loja não encontrada.")


    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Loja deletada com sucesso."}, 204
        except KeyError:
            abort(404, message="Loja não encontrada.")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}, 200


    def post(self):
        store_data = request.get_json()

        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="A Loja já existe.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "store_id": store_id}
        stores[store_id] = store
        return store, 201

