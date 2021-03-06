from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList

from db import db

#resource == stuffs that your api can return

app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #you can change the sqlite to any other db, the
#///means that we are in the root foulder of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app,authenticate,identity)

api.add_resource(Store, '/store/<string:name>')  
api.add_resource(Item, '/item/<string:name>')# the name is coming from get name
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister,'/userRegister')


app.run(port=5000, debug=False)
    