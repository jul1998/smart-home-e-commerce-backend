from ..db import db
import os


class Producto(db.Model):
    __tablename__="producto"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=True)
    stock = db.Column(db.Integer, unique = False, nullable=False)
    precio = db.Column(db.Numeric(precision=10, scale=2), unique=False)
    img_product = db.Column(db.Text(), unique= False, nullable=True)
    #parent_id = db.Column(db.Integer, db.Foreignkey('user.id'))
    favorite_product = db.relationship("FavoritoProductos", backref="producto") #favorite_product works as a list that contains all favorite products in child table FavoritoProductos
    shopping_cart = db.relationship("ShoppingCartItem", backref="producto")
    compras = db.relationship("Compras", backref="producto")
    reviews = db.relationship("Reviews", backref="producto")
    estado = db.Column(db.String(60), nullable = False)
    description = db.relationship("ProductDescription", backref="producto" )
    

    def __repr__(self):
        return '<Producto %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "stock": self.stock,
            "price": self.precio,
            "status": self.estado,
            "img": self.img_product
        }
    
    