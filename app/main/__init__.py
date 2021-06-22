# import and register blueprints
from flask import Blueprint

main = Blueprint('main', __name__)

# import any flask extension specific to this module

# import views
from app.main import views
