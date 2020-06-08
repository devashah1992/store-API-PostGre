from flask_restful import Resource, reqparse
from models.store import StoreModel
from flask import request

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted'}
        return {'message': 'Store not found'}, 404

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}


class FilterStore(Resource):

    def get(self):
        store_name = request.args.get('store_name')
        store = StoreModel.find_by_name(store_name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404
