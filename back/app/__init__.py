from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
# from dotenv import load_dotenv
import os
import yfinance as yf



db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@10.0.30.10:3306/finanse_db_dev"
    app.config['SECRET_KEY'] = 'super'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    CORS(app)


    
    

    # Konfiguracja bazy danych 

    db.init_app(app)

    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login' # Gdzie przekierować niezalogowanych
    login_manager.init_app(app)


    from app.routes.main import main_bp

    app.register_blueprint(main_bp)


    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)


    from app.routes.stocks import stocks_bp
    app.register_blueprint(stocks_bp)

    from app.routes.exchangeRates import exchanges_bp
    app.register_blueprint(exchanges_bp)


    with app.app_context():
        from app import models
        # db.create_all()  

    return app