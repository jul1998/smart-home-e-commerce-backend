from ..db import db
import os

class Compras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))
    costo = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    trackId = db.Column(db.String(250), unique=True)
    estadoEnvio = db.Column(db.String(60), nullable=False)
    problemas = db.relationship("Problemas", backref="compras")

    
    def __repr__(self):
        return '<Compras %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "fecha": self.email,
            "costo": self.name,
            "userId": self.userId,
            "productId": self.productId,
            "trackId": self.trackId,
            "estadoEnvio": self.estadoEnvio
        }
