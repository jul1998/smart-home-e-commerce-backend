from ..db import db
import os

class CarritoCompras(db.Model):
    __tablename__ = "carritoCompras"
    id = db.Column(db.Integer, primary_key=True)
    idOrder = db.Column(db.Integer, nullable = False) 
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad = db.Column(db.Integer, nullable = False)
    #costoUnitario = db.Column(db.Numeric(precision=10, scale=2), db.ForeignKey('producto.precio'))
    
    def __repr__(self):
        return '<CarritoCompras %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "idOrder": self.idOrder,
            "userId": self.userId,
            "productId": self.productId,
            "cantidad": self.cantidad,
            "costoUnitario": Producto.query.get(self.productId).serialize()['precio']
        }