from ..db import db
import os

class Compras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))
    costo = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    
