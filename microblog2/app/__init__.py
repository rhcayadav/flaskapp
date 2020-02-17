from flask import Flask
# , request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
#from flask_mysqldb import MySQL
from flask_login import LoginManager
from config import Config

# ...
db = SQLAlchemy()
#db = MySQL(app)
# db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.cluster import bp as cluster_bp
    app.register_blueprint(cluster_bp, url_prefix='/cluster')

    # ... no changes to blueprint registration

    #    if not app.debug and not app.testing:
    # ... no changes to logging setup

    return app

from app import models