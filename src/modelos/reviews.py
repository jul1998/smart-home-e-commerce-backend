from ..db import db
import os

class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))
    descripcion = db.Column(db.String(2000))
    calificacion = db.Column(db.Integer)
    estado = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<Reviews %r>' % self.productId

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "productId": self.productId,
            "descripcion": self.descripcion,
            "calificacion": self.calificacion
        }

