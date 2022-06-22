'''
    Набор функций, которые применяются в рамках hanlers
'''
from app import db, Error, ShopUnit
from flask import jsonify
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


def delete_child(id_child, id_parent):
    parent = ShopUnit.query.filter_by(id=id_parent).first()
    if parent:
        if parent.children is not None:
            ch = list(parent.children)
            ch.pop(ch.index(id_child))
            parent.children = set(ch)