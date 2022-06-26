from db import db
from flask import Blueprint
from components.schemas.ShopUnitType import ShopUnitType
from my_logs.logg import info_log

bp_consoly = Blueprint('commands', __name__)

from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


@bp_consoly.cli.command('create_db')
def create_db():
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
    from tests import test_run
    test_run(info_log)


@bp_consoly.cli.command('run_long_test')
def go_test():
    from tests import long_test_run
    long_test_run(info_log)
