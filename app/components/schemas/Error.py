from app.db import db

class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    message = db.Column(db.String(50))
