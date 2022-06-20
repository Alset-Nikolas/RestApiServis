from yandex_rest_api_server.ServisRestApi.enrollment import db


class NodeTree(db.Model):
    node_id = db.Column(db.String(), primary_key=True, nullable=False, unique=True, )
    parentId = db.Column(db.String())
    name = db.Column(db.String(), nullable=False)
    type_ = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer)
    time_ = db.Column(db.DateTime(), nullable=False)
    childs = db.Column(db.Integer)
