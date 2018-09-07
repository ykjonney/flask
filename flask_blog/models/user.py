from validators.database import db


class User(db.Model):
    __table__='user'
    username=db.Column(db.String(40),nullable=False)
    password=db.Column(db.String(120),nullable=False)
    email=db.Column(db.String(80),nullable=False)
    is_active=db.Column(db.Boolean,default=False)
    is_verify=db.Column(db.Boolean,default=False)