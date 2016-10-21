
import datetime

class SessionMixin(object):
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