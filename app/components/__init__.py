import datetime

from flask import Blueprint
from components.schemas.ShopUnitType import ShopUnitType
from components.schemas.ShopUnit import ShopUnit
from components.schemas.ShopUnitImport import ShopUnitImport
from components.schemas.ShopUnitImportRequest import ShopUnitImportRequest
from components.schemas.Error import Error
from components.schemas.ShopUnitStatistic import ShopUnitStatistic

bp_postgres = Blueprint('postgres', __name__)

# from app.main import db
# x=ShopUnitType.query.filter_by(type="new_type").first()
#
# x = ShopUnit(id="new_id", name='new_name', date=datetime.datetime.now(), type=x.type)
# db.session.add(x)
#
# db.session.commit()