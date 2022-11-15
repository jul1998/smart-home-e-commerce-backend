from ..db import db
import os

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=True)
    stock = db.Column(db.Integer, unique = False, nullable=False)
    precio = db.Column(db.Numeric(precision=10, scale=2), unique=False)
    #parent_id = db.Column(db.Integer, db.Foreignkey('user.id'))
    user_favorite = db.relationship("FavoritoProductos", backref="producto")
    carritoCompras = db.relationship("CarritoCompras", backref="producto")
    estado = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return '<Producto %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    