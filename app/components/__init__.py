from flask import Blueprint
from components.schemas.ShopUnitType import ShopUnitType
from components.schemas.ShopUnit import ShopUnit
from components.schemas.ShopUnitImport import ShopUnitImport
from components.schemas.ShopUnitImportRequest import ShopUnitImportRequest
from components.schemas.Error import Error
from components.schemas.ShopUnitStatisticUnit import ShopUnitStatisticUnit

bp_postgres = Blueprint('postgres', __name__)