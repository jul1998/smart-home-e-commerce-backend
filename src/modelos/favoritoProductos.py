from ..db import db
import os

class FavoritoProductos(db.Model):
    __tablename__ = "favoritoProductos"
    id = db.Column(db.Integer,  primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))

    def __repr__(self):
        return '<FavoritoProducto %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_email": User.query.get(self.userId).serialize()['email'],
            "producto_name": People.query.get(self.productoId).serialize()['name']          
        }