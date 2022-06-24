from db import db


class ShopUnitImport(db.Model):
    id = db.Column(db.String(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    parentId = db.Column(db.String(), nullable=True)
    type = db.Column(db.String(), db.ForeignKey('shop_unit_type.type'), nullable=False)
    price = db.Column(db.Integer, nullable=True)

    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type

    def __repr__(self):
        return f'id={self.id}; name={self.name}; date={self.date};'
