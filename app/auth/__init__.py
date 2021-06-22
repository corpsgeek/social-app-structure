from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import auth_forms, auth_views, auth_utils
