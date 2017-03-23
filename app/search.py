# -*- coding: utf-8 -*-

from flask import request
from app import db
from app.utils import pagination

class Search(object):
    def __init__(self, **kwargs):
        self.keys = []
        for (key, value) in request.args.items():
            setattr(self, key, value)
            self.keys.append(key)
        for (key, value) in kwargs.items():
            setattr(self, key, value)
            self.keys.append(key)

    def load(self, model):
        self.query = model.query
        for k in self.keys:
            if hasattr(model, 'search_fields') and k in getattr(model, 'search_fields'):
                if k.endswith('_like'):
                    key = k.replace('_like', '')
                    self.query = self.query.filter(getattr(model, key).like('%{}%'.format(getattr(self, k))))
                elif k.endswith('_begin'):
                    key = k.replace('_begin', '')
                    self.query = self.query.filter(getattr(model, key) >= getattr(self, k))
                elif k.endswith('_end'):
                    key = k.replace('_end', '')
                    self.query = self.query.filter(getattr(model, key) <= getattr(self, k))
                else:
                    self.query = self.query.filter(getattr(model, k)==getattr(self, k))
        return self

    def paginate(self):
        return pagination(self.query)
