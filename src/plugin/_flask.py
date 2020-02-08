# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask._compat import text_type, string_types
from flask.json import JSONEncoder
from decimal import Decimal
import json, datetime

# 自动识别字典，转换成json
def make_response(self, rv):
    status_or_headers = headers = None
    if isinstance(rv, tuple):
        rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))

    if rv is None:
        raise ValueError('View function did not return a response')

    if isinstance(status_or_headers, (dict, list)):
        headers, status_or_headers = status_or_headers, None

    if not isinstance(rv, self.response_class):
        # When we create a response object directly, we let the constructor
        # set the headers and status.  We do this because there can be
        # some extra logic involved when creating these objects with
        # specific values (like default content type selection).
        if isinstance(rv, (text_type, bytes, bytearray)):
            rv = self.response_class(rv, headers=headers,
                                        status=status_or_headers)
            headers = status_or_headers = None
        elif isinstance(rv, dict):
            rv = jsonify(rv)
        else:
            rv = self.response_class.force_type(rv, request.environ)

    if status_or_headers is not None:
        if isinstance(status_or_headers, string_types):
            rv.status = status_or_headers
        else:
            rv.status_code = status_or_headers
    if headers:
        rv.headers.extend(headers)

    return rv

def extends_db(db):
    class JsonBlob(db.TypeDecorator):
        impl = db.Text

        def process_bind_param(self, value, dialect):
            if isinstance(value, str):
                return value
            return json.dumps(value, ensure_ascii=False)

        def process_result_value(self, value, dialect):
            if value is not None:
                if not value:
                    return None
                return json.loads(value)
            return None

    class MoneyBlob(db.TypeDecorator):
        impl = db.Integer

        def process_bind_param(self, value, dialect):
            return float(value) * 100

        def process_result_value(self, value, dialect):
            return value / 100

    db.JsonBlob = JsonBlob
    db.MoneyBlob = MoneyBlob

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime.datetime):
                if obj.strftime('%Y-%m-%d %H:%M:%S') == '1970-01-01 00:00:00':
                    return ''
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(obj, datetime.date):
                if obj.strftime('%Y-%m-%d') == '1970-01-01':
                    return ''
                return obj.strftime('%Y-%m-%d')
            if isinstance(obj, Decimal):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)