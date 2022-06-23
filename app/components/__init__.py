from flask import Blueprint
from app.components.schemas.ShopUnitType import ShopUnitType
from app.components.schemas.ShopUnit import ShopUnit
from app.components.schemas.ShopUnitImport import ShopUnitImport
from app.components.schemas.ShopUnitImportRequest import ShopUnitImportRequest
from app.components.schemas.Error import Error
from app.components.schemas.ShopUnitStatisticUnit import ShopUnitStatisticUnit

bp_postgres = Blueprint('postgres', __name__)