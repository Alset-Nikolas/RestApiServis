import datetime

print('app.__init__')
from flask import Flask
from app.components import create_app

app = Flask(__name__)
db = create_app(app)

from app.components.schemas.ShopUnitType import ShopUnitType
from app.components.schemas.ShopUnit import ShopUnit
from app.components.schemas.ShopUnitImport import ShopUnitImport
from app.components.schemas.ShopUnitImportRequest import ShopUnitImportRequest
from app.components.schemas.Error import Error
from app.components.schemas.ShopUnitStatisticUnit import ShopUnitStatisticUnit
# from app.components.schemas.ShopUnitStatisticResponse import ShopUnitStatisticResponse

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
#
