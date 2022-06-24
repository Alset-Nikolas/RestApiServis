from db import db


class ShopUnitStatisticResponse(db.Model):
    id = db.Column(db.String(), primary_key=True, nullable=False)
    items = db.Column(
        db.ARRAY(db.String(), db.ForeignKey('shop_unit_statistic_unit.id', 'shop_unit_statistic_unit.date')),
        nullable=False)

    # __table_args__ = (db.ForeignKeyConstraint([author_firstName, author_lastName],
    #                                        [Author.firstName, Author.lastName]),
    #                   {})

    def __repr__(self):
        return f'id={self.id} ,items={self.items}'
