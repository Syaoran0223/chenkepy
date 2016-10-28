
import datetime
from app import db

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