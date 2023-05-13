from flask import request, make_response, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel, StoreModel
from db import db

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Um erro ocorreu ao inserir o item.")

        item_dto = {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "store": {
                "id": item.store.id,
                "name": item.store.name,
            }
        }

        return make_response(jsonify(item_dto), 201)


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.filter(ItemModel.id == item_id).first()

        if item is None:
            return make_response(jsonify({"message": "Item não encontrado"}), 404)

        store = StoreModel.query.filter(StoreModel.id == item.store_id).first()

        item_dto = {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "store_id": item.store_id,
            "store": {
                "id": store.id,
                "name": store.name,
            },
        }

        return make_response(jsonify(item_dto), 200)

    @blp.response(201, ItemSchema)
    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        item_dto = {}

        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]

            store = StoreModel.query.filter(StoreModel.id == item.store_id).first()

            item_dto = {
                "name": item.name,
                "price": item.price,
                "store": {
                    "id": store.id,
                    "name": store.name,
                }
            }
        else:
            return make_response(jsonify({"message": "Item não encontrado"}), 404)

        return make_response(jsonify(item_dto), 201)

    def delete(self, item_id):
        item = ItemModel.query.filter(ItemModel.id == item_id).first()

        if item is None:
            return make_response(jsonify({"message": "Item não encontrado."}), 404)

        db.session.delete(item)
        db.session.commit()

        return make_response(jsonify({"message": "Item excluído com sucesso."}), 204)