
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.store import StoreModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This field cannot be left blank"
            )
    parser.add_argument('store_id',
                            type=int,
                            required=True,
                            help="All Items need an Store<StoreID>"
            )
   
    
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.search_item( name)
        
        if item: 
            return item.json()
        return {'message':'item not found'},404
            
    def post(self, name):
        if ItemModel.search_item(name) is not None:
            return {'message':'the item {} already exists'.format(name)},400
        
        data = Item.parser.parse_args()
        
        if StoreModel.search_store_by_id(data['store_id']) is None:
            return {'message':'the store {} does not exists'.format(data['store_id'])},400
        
        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {'message':'Something has go wrong'},500
        
        return item.json(), 201
    
    def delete(self,name):
        item = ItemModel.search_item(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}
    
    def put(self,name):
        data = Item.parser.parse_args()

        item = ItemModel.search_item(name)
        
        if item is None:
            item = ItemModel(name,**data)  
           
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        
        if StoreModel.search_store_by_id(data['store_id']) is None:
            return {'message':'the store {} does not exists'.format(data['store_id'])},400

        item.save_to_db()
        return item.json()
        
    
class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        return {'items':[item.json() for item in items ]}, 200
    
    def post(self,name):
        pass