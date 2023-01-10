from ..db import db
import os

class Comments(db.Model):
    __tablename__="comments"
    id = db.Column(db.Integer, primary_key=True)
    posted_by_userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", back_populates="product_comments")#References User table
    productId = db.Column(db.Integer, db.ForeignKey('producto.id'))
    posted_at = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.Text, nullable=False)

    def serialize(self):
        return ({
            "id": self.id,
            "posted_by":self.posted_by_userid,
            "author":self.author.name,
            "author_img": self.author.img_profile,
            "product_id": self.productId,
            "posted_at": self.posted_at,
            "comment": self.comment
        })