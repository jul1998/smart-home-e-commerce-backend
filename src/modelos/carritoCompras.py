from ..db import db
import os
from ..modelos import Producto

class ShoppingCart(db.Model):
    __tablename__ = "shoppingCart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    #idOrder = db.Column(db.Integer, nullable = False) 
    #userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    #cantidad = db.Column(db.Integer, nullable = False)
    #costoUnitario = db.Column(db.Numeric(precision=10, scale=2), db.ForeignKey('producto.precio'))
    
    def __repr__(self):
        return '<CarritoCompras %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

    #def serialize(self):
    #    return {
    #        "id": self.id,
    #        "idOrder": self.idOrder,
    #        "userId": self.userId,
    #        "productId": self.productId,
    #       "cantidad": self.cantidad,
    #       "price": Producto.query.get(self.productId).serialize()['price'],
    #        "name": Producto.query.get(self.productId).serialize()['name']
    #    }

class ShoppingCartItem(db.Model):
    __tablename__ = "shoppingCartItem"
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user_cart = db.relationship("User", backref="shoppingCartItem")
    shopping_cart_id = db.Column(db.Integer, db.ForeignKey('shoppingCart.id'))
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))
    product_name = db.relationship("Producto", backref="shoppingCartItem")
    product_price = db.Column(db.Float, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)

    
    def __repr__(self):
        return '<shoppingCartItem %r>' % self.product_name

    def serialize(self):
        return {
            "id": self.id,
            #"user_cart": self.user_cart.name,
            "productId": self.productId,
            "product_name": self.product_name.name,
            "product_price": self.product_price,
            "quantity":self.product_quantity
        }