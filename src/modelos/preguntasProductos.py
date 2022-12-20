from ..db import db
import os


class PreguntasProductos(db.Model):
    __tablename__ = "preguntasproductos"
    id = db.Column(db.Integer, primary_key=True)
    ask_by_userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", back_populates="product_questions")#References User table
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))
    descripcion = db.Column(db.String(2000))
    posted_at = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return '<PreguntasProductos %r>' % self.ask_by_userid

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.ask_by_userid,
            "productId": self.productId,
            "descripcion": self.descripcion,
            "posted_at": self.posted_at,
            "author":self.author.name
        }

