from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    def get(self,name):
        store = StoreModel.search_store(name)
        if store:
            return store.json()
        return {'message':'Store not found'}, 404# in this line we are basically
    # returning an tuple with the body response and the status code response,
    # an does not exist the status the default is 200
    
    def post(self,name):
        if StoreModel.search_store(name):
            return {'Message':"The Store '{}' already exists".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'An error occurred in our side'}, 500
        
        return store.json(),201#= CREATED
        
    
    def delete(self, name):
        if StoreModel.search_store(name) is None:
             return {'Message':"The Store '{}' does not exists".format(name)}, 400
        
        store = StoreModel.search_store(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}
    # def delete(self,name):
    #    if StoreModel.search_store(name) is None:
    #         return {'Message':"The Store '{}' does not exists".format(name)}, 400
        
    #    store = StoreModel(name)
    #    try:
    #         store.delete_from_db()
    #    except:
    #        return {'message':'An error occurred in our side'}, 500
        
    #    return {'message': 'the store was deleted sucessfullt'}
        
         
    
class StoreList(Resource):
    def get(self):
        stores = StoreModel.query.all()
        return {'Stores':[store.json() for store in stores ]}, 200
    