from ..db import db
import os

class FavoritoProductos(db.Model):
    __tablename__ = "favoritoProductos"
    id = db.Column(db.Integer,  primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_product = db.relationship("User", back_populates="user_favorites")#user_product is now a User object where we can access any attribute in User
    product = db.relationship("Producto", back_populates="favorite_product")#product is now a Producto object where we can access any attribute in Producto
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))

    def __repr__(self):
        return '<FavoritoProductos %r>' % self.productId

    def serialize(self):
        return {
            "id": self.id,
            "user_email": User.query.get(self.userId).serialize()['email']     
        }