print('ShopUnitImportRequest')

from app import db

class ShopUnitImportRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.ARRAY(db.String(), db.ForeignKey('shop_unit_import.id')),nullable=False)
    updateDate = db.Column(db.DateTime, nullable=False)


