from datetime import datetime
import sqlalchemy as sm
from flask_sqlalchemy import SQLAlchemy,BaseQuery
from flask_sqlalchemy.model import Model
from sqlalchemy.ext.declarative import declared_attr


class QueryWithSoftDelete(BaseQuery):
    def __new__(cls, *args, **kwargs):
       obj= super(QueryWithSoftDelete,cls).__new__(cls)
       obj._with_deleted=kwargs.pop('_with_deleted',False)
       if len(args)>0:
           super(QueryWithSoftDelete, obj).__init__(*args,**kwargs)
           return obj.filter_by(deleted_at=None)if not obj._with_deleted else obj
       return obj
    def __init__(self):
        pass
    def with_delete(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),session=db.session(),_with_deleted=True)
    def _get(self,*args,**kwargs):
        return super(QueryWithSoftDelete,self).get(*args,**kwargs)
    def get(self,*args,**kwargs):
        obj=self.with_delete()._get(*args,**kwargs)
        if obj is None or self._with_deleted or not obj.deleted_at:
            return obj
        return None

class MetaModel(Model):
    @declared_attr
    def id(cls):
       for base in cls.__mro__[1:-1]:
          if getattr(base,'__table__',None) is not None:
             type=sm.ForeignKey(base.id)
          else:
             type=sm.Integer
       return sm.Cloumn(type,primary_key=True)

    @declared_attr
    def create_at(_):
       return sm.Column(sm.DateTime,default=datetime.utcnow(),nullable=False)

    @declared_attr
    def update_at(_):
       return sm.Column(sm.DateTime,onupdate=datetime.utcnow())

    @declared_attr
    def deleted_at(_):
       return sm.Column(sm.DateTime)
    def save(self,commit=True):
       db.session.add(self)
       if commit:
           db.session.commit()
       return self
    def update(self,commit=True,**kwargs):
       kwargs.pop("id",None)
       for attr,val in kwargs.items():
           if val is not None:
              setattr(self,attr,val)
       return commit and self.save() or self
    def delete(self,commit=True):
       self.deleted_at=datetime.utcnow()
       return commit and self.save()
def __reference_col(tablename,nullable=False,pk_name=id,**kwargs):
    return db.Column(db.ForeignKey("{}.{}").format(tablename,pk_name),nullable=nullable,**kwargs)
db =SQLAlchemy(query_class=QueryWithSoftDelete,model_class=MetaModel)
db.Reference_col=__reference_col

