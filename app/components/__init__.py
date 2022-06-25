from flask import Blueprint
from components.schemas.ShopUnitType import ShopUnitType
from components.schemas.ShopUnit import ShopUnit
from components.schemas.ShopUnitImport import ShopUnitImport
from components.schemas.ShopUnitImportRequest import ShopUnitImportRequest
from components.schemas.Error import Error
from components.schemas.ShopUnitStatistic import ShopUnitStatistic
# from components.schemas.ShopUnitStatisticResponse import ShopUnitStatisticResponse
bp_postgres = Blueprint('postgres', __name__)
