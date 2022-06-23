from app import db


class ShopUnit(db.Model):
    id = db.Column(db.String(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    parentId = db.Column(db.String(), nullable=True)
    type_id = db.Column(db.String(), db.ForeignKey('shop_unit_type.type'), nullable=False)
    type = db.relationship('ShopUnitType', backref=db.backref('units', lazy=True))
    price = db.Column(db.Integer, nullable=True)
    children = db.Column(db.ARRAY(db.String(), db.ForeignKey('shop_unit.id')), nullable=True)

    def __init__(self, id, name, date, type):
        self.id = id
        self.name = name
        self.date = date
        self.type = type


    def __repr__(self):
        return f'id={self.id}; name={self.name}; date={self.date}; type={self.type}'
