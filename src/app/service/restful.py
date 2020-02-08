from flask import request
from app.service.search import Search

def post(Model):
    data = request.json
    obj = Model.create(data)
    return obj.to_dict()

def put(Model, id):
    obj = Model.query.get_or_404(id)
    data = request.json
    obj = obj.update(data)
    return obj.to_dict()

def delete(Model, id):
    obj = Model.query.get_or_404(id)
    obj.delete()
    return {}

def get_one(Model, id):
    obj = Model.query.get_or_404(id)
    return obj.to_dict()

def get(Model):
    search = Search()
    res = search.load(Model).paginate()
    return res

