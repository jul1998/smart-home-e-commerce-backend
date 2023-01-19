from ..db import db
import os

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="tickets")
    description = db.Column(db.Text)
    posted_at = db.Column(db.DateTime, nullable=False)


    def serialize(self):
        return ({
            "id": self.id,
            "user_id": self.user_id,
            "user_email": self.user.email,
            "description": self.description,
            "date": self.posted_at 
        })