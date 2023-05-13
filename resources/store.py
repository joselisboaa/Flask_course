import uuid
from flask import request, make_response, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from schemas import StoreSchema
from models import StoreModel, ItemModel
from db import db

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.filter(StoreModel.id == store_id).first()
        if store is None:
            return make_response(jsonify({"message": "Loja não existente."}), 404)

        store_dto = {
            "id": store.id,
            "name": store.name,
            "items": [],
        }

        items = ItemModel.query.filter(ItemModel.store_id == store.id)
        for item in items:
            item_dto = {
                "id": item.id,
                "name": item.name,
                "price": item.price,
            }

            store_dto["items"].append(item_dto)

        return make_response(jsonify(store_dto), 200)

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)

        if store is None:
            return make_response(jsonify({"message": "Loja não encontrada"}), 404)
        else:
            store.name = store_data["name"]

        store_dto = {
            "name": store.name,
            "items": [],
        }

        for itens in store.items:
            item_dto = {
                "id": itens.id,
                "name": itens.name,
                "price": itens.price,
            }

            store_dto["items"].append(item_dto)

        db.session.add(store)
        db.session.commit()

        return make_response(jsonify(store_dto), 201)

    def delete(self, store_id):
        store = StoreModel.query.filter(StoreModel.id == store_id).first()

        if store is None:
            return make_response(jsonify({"message": "Loja não encontrada."}), 404)

        db.session.delete(store)
        db.session.commit()

        return make_response(jsonify({"message": "Loja excluída com sucesso"}), 204)


@blp.route("/store")
class StoreList(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def get(self):
        return StoreModel.query.all()


    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "Error.")
        return store
