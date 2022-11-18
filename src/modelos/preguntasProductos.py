from ..db import db
import os


class PreguntasProductos(db.Model):
    __tablename__ = "preguntasproductos"
    id = db.Column(db.Integer, primary_key=True)
    ask_by_userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))
    descripcion = db.Column(db.String(2000))
    posted_at = db.Column(db.DateTime, nullable=False)
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

