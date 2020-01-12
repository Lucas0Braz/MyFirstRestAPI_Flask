from db import db
import sys


class StoreModel(db.Model):
    
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy='dynamic')
    # when we put lazy=dynamic, isto pega o que era 
    #antes uma lista de items de cada store 
    #e transforma em um query builder
     
    def __init__(self,name):
        self.name = name
        
        
    def json(self):
        return {'id':self.id,'name':self.name,'items': [item.json() for item in self.items.all()]}
     
    @classmethod
    def search_store(cls,name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def search_store_by_id(cls,id):
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()   
        