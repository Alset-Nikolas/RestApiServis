
from app import db


class ShopUnitStatisticUnit(db.Model):
    id = db.Column(db.String(), primary_key=True, nullable=False)
    date = db.Column(db.DateTime)
    name = db.Column(db.String(), nullable=False)
    parentId = db.Column(db.String(), nullable=True)
    type = db.Column(db.String(), db.ForeignKey('shop_unit_type.type'), nullable=False)
    price = db.Column(db.Integer, nullable=True)

    def __init__(self, id, name, type, date):
        self.type = type
        self.date = date
        self.id = id
        self.name = name

    def __repr__(self):
        return f'id={self.id}; name={self.name}; date={self.date}; type={self.type}'
