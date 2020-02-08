# coding: utf-8

from flask import Blueprint

client_blueprint = Blueprint('client', __name__)

from . import login, project