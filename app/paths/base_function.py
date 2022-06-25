'''
    Набор функций, которые применяются в рамках hanlers
'''
from db import db
from components.schemas.Error import Error
from components.schemas.ShopUnit import ShopUnit
from flask import jsonify

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
def response_error_400():
    db.session.rollback()
    db.session.add(Error(code=400, message='Validation Failed'))
    db.session.commit()
    return jsonify({"code": 400, "message": "Validation Failed"}), 400


def response_error_404():
    db.session.rollback()
    db.session.add(Error(code=404, message="Item not found"))
    db.session.commit()
    return jsonify({"code": 404, "message": "Item not found"}), 404


def delete_child(id_child: str, id_parent: object) -> None:
    parent = ShopUnit.query.filter_by(id=id_parent).first()
    if parent:
        if parent.children is not None:
            ch = list(parent.children)
            ch.pop(ch.index(id_child))
            parent.children = set(ch)

