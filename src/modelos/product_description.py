from ..db import db
import os

class ProductDescription(db.Model):
    __tablename__ = "productDescription"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150), unique=False, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    product = db.relationship("Producto", back_populates="description")

    def __repr__(self):
        return '<Producto %r>' % self.description

    def serialize(self):
        return {
            "description": self.description
        }
    