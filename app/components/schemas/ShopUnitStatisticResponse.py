from db import db


class ShopUnitStatisticResponse(db.Model):
    id = db.Column(db.String(), primary_key=True, nullable=False)
    items = db.Column(db.ARRAY(db.String(), db.String()), nullable=False)
    # , 'shop_unit_statistic_unit.date'
    __table_args__ = (db.ForeignKeyConstraint(['items', 'items'],
                                           ['shop_unit_static.id', "shop_unit_static.id"]),
                      {})

    def __repr__(self):
        return f'id={self.id} ,items={self.items}'
