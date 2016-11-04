
import datetime
from app import db
from flask.ext.sqlalchemy import BaseQuery

class SessionMixin(object):
    created_at = db.Column('created_at', db.DateTime, nullable=False)
    updated_at = db.Column('updated_at', db.DateTime, nullable=False)

    @staticmethod
    def create_time(mapper, connection, instance):
        now = datetime.datetime.now()
        instance.created_at = now
        instance.updated_at = now

    @staticmethod
    def update_time(mapper, connection, instance):
        now = datetime.datetime.now()
        instance.updated_at = now

    @classmethod
    def register(cls):
        db.event.listen(cls, 'before_insert', cls.create_time)
        db.event.listen(cls, 'before_update', cls.update_time)

    def to_dict(self, filter=None):
        dictionary = self.__dict__.copy()
        res = {}
        for k, v in dictionary.items():
            if k == '_sa_instance_state':
                continue
            if k in getattr(self, 'protected_field', ()):
                continue
            if isinstance(filter, list) and k in filter:
                continue
            if isinstance(v, datetime.datetime):
                v = v.strftime('%Y-%m-%d %H:%M:%S')
            res[k] = v
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def bind_auto(cls, items, keys, refer_id='', id='id', prefix=''):
        res = []
        if not refer_id:
            refer_id = cls.__tablename__ + '_id'
        if not isinstance(keys, list):
            keys = [keys]
        if not isinstance(items, list):
            if not isinstance(items, dict):
                raise ValueError('need dict')
            r_id = items.get(refer_id, 0)
            obj = cls.query.get(r_id)
            for key in keys:
                prefix = cls.__tablename__ if not prefix else prefix
                ref_key = prefix + '_' + key
                if not obj:
                    items[ref_key] = ''
                else:
                    items[ref_key] = getattr(obj, key)
            return items
        r_ids = [data.get(refer_id, 0) for data in items]
        objs = cls.query.filter(cls.id.in_(r_ids)).all()
        for item in items:
            if not isinstance(item, dict):
                raise ValueError('need dict')
            obj = list(filter(lambda x: x.id==item.get(refer_id, 0), objs))
            for key in keys:
                prefix = cls.__tablename__ if not prefix else prefix
                ref_key = prefix + '_' + key
                if len(obj):
                    item[ref_key] = getattr(obj[0], key)
                else:
                    item[ref_key] = ''
            res.append(item)
        return res
            

