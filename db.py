from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    alive = db.Column(db.Boolean, nullable=False)
    target = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.alive = True
        self.target = -1

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'alive': self.alive,
            'target': self.target,
        }
