import datetime
from flask import request, g
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.attributes import InstrumentedAttribute
from cerberus import Validator

from app import db
from app.service.search import Search
from app.service.utils import api_success
from plugin.exceptions import ApiError, NotFoundError

class SessionWithoutTimeMixin(object):
    # 生成对象时忽略的字段
    global_ignore_assemble_fields = ['id', 'is_delete']
    # 更新时忽略的字段
    ignore_update_fields = []
    v = None

    def to_dict(self, filter=None):
        attrs = dir(self)
        remove_fileds = getattr(self, 'protected_field', [])
        res = {}
        for attr in attrs:
            if not isinstance(getattr(self.__class__, attr, ''), InstrumentedAttribute):
                continue
            if attr in remove_fileds:
                continue
            value = getattr(self, attr)
            res[attr] = value
        return res

    def pick(self, *args):
        attrs = args
        res = {}
        for attr in attrs:
            if not isinstance(getattr(self.__class__, attr, ''), InstrumentedAttribute):
                continue
            value = getattr(self, attr)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
                if value == '1970-01-01 00:00:00':
                    value = ''
            if isinstance(value, datetime.date):
                value = value.strftime('%Y-%m-%d')
            res[attr] = value
        return res

    @classmethod
    def generate_validator(cls):
        if not cls.v:
            cls.v = Validator(getattr(cls, 'schema', {}))
            cls.v.allow_unknown = True
        return cls.v

    # 根据data组装对象
    @classmethod
    def assemble(cls, data, obj=None):
        v = cls.generate_validator()
        update = True if obj else False
        if not v.validate(data, update=update):
            raise ApiError(v.errors)
        obj = obj or cls()
        attrs = dir(obj)
        keys = data.keys()
        for key in keys:
            if key in cls.global_ignore_assemble_fields:
                continue
            if isinstance(getattr(cls, key, ''), InstrumentedAttribute)\
                    or isinstance(getattr(cls, key, ''), property):
                setattr(obj, key, data[key])
        return obj

    @classmethod
    def create(cls, data):
        obj = cls.assemble(data)
        obj.save()
        return obj

    def update(self, data):
        data_keys = data.keys()
        for field in self.ignore_update_fields:
            if field in data_keys:
                del(data[field])
        obj = self.__class__.assemble(data, self)
        obj.save()
        return obj

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def soft_delete(self):
        self.is_delete = True
        self.save()
        return self

    @classmethod
    def rest_post(cls):
        data = request.json
        obj = cls.create(data)
        res = obj.to_dict()
        return api_success(res)

    @classmethod
    def rest_delete(cls, id):
        obj = cls.query.get_or_404(id)
        obj.delete()
        return api_success({})

    @classmethod
    def rest_soft_delete(cls, id):
        obj = cls.query.get_or_404(id)
        obj.soft_delete()
        return api_success({})

    @classmethod
    def rest_get_one(cls, id):
        obj = cls.query.get_or_404(id)
        if hasattr(obj, 'is_delete') and obj.is_delete:
            raise NotFoundError()
        return api_success(obj.to_dict())

    @classmethod
    def get_one(cls, id):
        obj = cls.query.get_or_404(id)
        if hasattr(obj, 'is_delete') and obj.is_delete:
            raise NotFoundError()
        return obj

    @classmethod
    def rest_get(cls):
        search = Search()
        res = search.load(cls).paginate()
        return api_success(res)
    
    @classmethod
    def rest_put(cls, id):
        obj = cls.query.get_or_404(id)
        data = request.json
        obj = obj.update(data)
        return api_success(obj.to_dict())

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

class SessionMixin(SessionWithoutTimeMixin):
    created_at = db.Column('created_at', db.DateTime, nullable=False,
        default=datetime.datetime.now)
    updated_at = db.Column('updated_at', db.DateTime, nullable=False,
        default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # 生成对象时忽略的字段
    global_ignore_assemble_fields = ['id', 'created_at', 'updated_at', 'is_delete']

class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(is_delete=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.is_delete else None