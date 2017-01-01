# coding: utf-8

from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

from . import views, review, preprocess_view, input, answer, answer_check, judge, verify
