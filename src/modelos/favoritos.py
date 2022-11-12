from ..db import db
import os

class FavoritoProductos(db.Model):
    __tablename__ = "favoritoProductos"
    id = db.Column(db.Integer,  primary_key=True)
    userId = db.Column(db.Integer, db.foreignKey('user.id'))
    productId = db.Column(db.Integer, db.foreignKey('producto.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user_email": User.query.get(self.userId).serialize()['email'],
            "producto_name": People.query.get(self.productoId).serialize()['name']          
        }