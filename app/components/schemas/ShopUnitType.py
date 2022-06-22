print('app.scheas.2')

from app import db

class ShopUnitType(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), unique=True, primary_key=True)

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f'type={self.type}'
