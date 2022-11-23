from ..db import db
import os


class AdminUser(db.Model):
    __tablename__ = "adminuser"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    name = db.Column(db.String(60), unique=False, nullable=True)
    phone = db.Column(db.Integer, unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    estado = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return '<AdminUser %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "phone": self.phone
            # do not. serialize the password, its a security breach
        }

