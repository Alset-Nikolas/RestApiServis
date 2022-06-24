from db import db


class ShopUnitStatistic(db.Model):
    id = db.Column(db.String(), primary_key=True, nullable=False, autoincrement=False, )
    date = db.Column(db.DateTime, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    parentId = db.Column(db.String(), nullable=True)
    type = db.Column(db.String(), db.ForeignKey('shop_unit_type.type'), nullable=False)
    price = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.UniqueConstraint("id", "date"),
    )

    def __init__(self, id, name, type, date):
        self.type = type
        self.date = date
        self.id = id
        self.name = name

    def __repr__(self):
        return f'id={self.id}; name={self.name}; date={self.date}; type={self.type}'
