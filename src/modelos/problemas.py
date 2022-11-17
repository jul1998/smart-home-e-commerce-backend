from ..db import db
import os

class Problemas(db.Model):
    __tablename__ = "problemas"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    compraId = db.Column(db.Integer, db.ForeignKey('compras.id'))
    descripcion = db.Column(db.String(2000))
    estado = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return '<Problemas %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "compraId": self.compraId,
            "descripcion": self.descripcion,
            "estado": self.estado
        }
