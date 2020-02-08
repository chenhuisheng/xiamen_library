# -*- coding: utf-8 -*-

from flask import request
from app import db
from app.service.utils import pagination

class Search(object):
    def __init__(self, **kwargs):
        self.query = None
        self.keys = []
        self.with_keys = ''
        self.with_model = None
        self.with_refer_id = ''
        self.with_id = 'id'
        self.with_prefix = ''
        for (key, value) in request.args.items():
            setattr(self, key, value)
            self.keys.append(key)
        for (key, value) in kwargs.items():
            setattr(self, key, value)
            self.keys.append(key)

    def init_query(self, query):
        self.query = query
        return self

    def load(self, model):
        self.query = self.query or model.query# 默认筛选
        if hasattr(model, 'search_fields_default'):
            for (key, operater, value) in model.search_fields_default:
                if operater == '==':
                    self.query = self.query.filter(getattr(model, key)==value)
                elif operater == '!=':
                    self.query = self.query.filter(getattr(model, key)!=value)
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
        if hasattr(model, 'created_at'):
            self.query = self.query.order_by(model.created_at.desc())
        if hasattr(model, 'is_delete'):
            self.query = self.query.filter(model.is_delete==False)
        return self

    def paginate(self, to_dict=True):
        res = pagination(self.query, None, to_dict)
        if self.with_model:
            items = res['items']
            items = self.with_model.bind_auto(items, self.with_keys, self.with_refer_id, self.with_id, self.with_prefix)
            res['items'] = items
        return res
    
    def all(self, to_dict=True):
        res = self.query.all()
        to_dict_func = 'to_dict'
        if to_dict:
            if isinstance(to_dict, str):
                to_dict_func = to_dict
            res = [getattr(d, to_dict_func)() for d in res]
        return {
            'items': res
        }

    def with_(self, model, keys, refer_id='', id='id', prefix=''):
        self.with_model = model
        self.with_keys = keys
        self.with_refer_id = refer_id
        self.with_id = id
        self.with_prefix = prefix
        return self
