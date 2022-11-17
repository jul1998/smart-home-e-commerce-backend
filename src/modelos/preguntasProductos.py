from ..db import db
import os


class PreguntasProductos(db.Model):
    __tablename__ = "preguntasproductos"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))
    descripcion = db.Column(db.String(2000))
    estado = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return '<PreguntasProductos %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "productId": self.productId,
            "descripcion": self.descripcion
        }

