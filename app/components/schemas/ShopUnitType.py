from db import db


class ShopUnitType(db.Model):
    type = db.Column(db.String(50), unique=True, primary_key=True, nullable=False)

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f'type={self.type}'
