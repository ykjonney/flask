import sqlalchemy as sa
from datetime import datetime
from flask import session
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_sqlalchemy.model import DefaultMeta, Model
from sqlalchemy.ext.declarative import declared_attr, declarative_base

# from flying_cash.compat import basestring


class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(
                deleted_at=None) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        obj = self.with_deleted()._get(*args, **kwargs)
        if obj is None or self._with_deleted or not obj.deleted_at:
            return obj
        return None


class MetaModel(Model):
    @declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                type = sa.ForeignKey(base.id)
                break
        else:
            type = sa.Integer

        return sa.Column(type, primary_key=True)

    @declared_attr
    def created_at(_):
        return sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def updated_at(_):
        return sa.Column(sa.DateTime, onupdate=datetime.utcnow)

    @declared_attr
    def deleted_at(_):
        return sa.Column(sa.DateTime)

    def update(self, commit=True, **kwargs):
        kwargs.pop('id', None)
        for attr, value in kwargs.items():
            if value is not None:
                setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        self.deleted_at = datetime.now()
        db.session.add(self)
        return commit and db.session.commit()


def __reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    return db.Column(db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
                     nullable=nullable, **kwargs)


db = SQLAlchemy(query_class=QueryWithSoftDelete, model_class=MetaModel)
db.ReferenceCol = __reference_col
