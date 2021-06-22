from flask import Flask
from flask_migrate import Migrate
from config import DevelopmentConfig

# import extensions instance
from app.models import db
from app.models import login_manager
from flask_mail import Mail

# instance of migrate flask
migrate = Migrate()
mail = Mail()


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    # initialize extension instances
    db.init_app(app)
    db.app = app

    # migrate initialization
    migrate.init_app(app, db)
    migrate.app = app

    # login manager initialization
    login_manager.init_app(app)
    login_manager.app = app

    # mail initialization
    mail.init_app(app)
    mail.app = app

    
    # register blueprints of applications
    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    # register error blueprint
    from app.errors import errors as errors_bp
    app.register_blueprint(errors_bp)

    # register the authentication blueprint
    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    return app
