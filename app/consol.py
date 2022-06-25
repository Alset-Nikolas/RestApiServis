from db import db
from flask import Blueprint
from components.schemas.ShopUnitType import ShopUnitType

bp_consoly = Blueprint('commands', __name__)


@bp_consoly.cli.command('create_db')
def create_db():
    print('Create Table')
    db.drop_all()
    db.create_all()

    CATEGORY = ShopUnitType.query.filter_by(type='CATEGORY').first()
    OFFER = ShopUnitType.query.filter_by(type='OFFER').first()

    if CATEGORY is None:
        CATEGORY = ShopUnitType(type='CATEGORY')
        db.session.add(CATEGORY)

    if OFFER is None:
        OFFER = ShopUnitType(type='OFFER')
        db.session.add(OFFER)

    db.session.commit()


@bp_consoly.cli.command('run_test')
def go_test():
    print('RUN TEST')
    create_db()
    from tests import test_run
    test_run()
