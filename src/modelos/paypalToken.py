from ..db import db
import os

class PaypalToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    tokenStatus = db.Column(db.Boolean, nullable=False)

    def serialize(self):
        return ({
            "id": self.id,
            "token": self.token,
            "created_at": self.created_at,
            "tokenStatus": self.tokenStatus
        })
