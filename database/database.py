from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

db = SQLAlchemy()
Base = declarative_base()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_activities.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        Base.metadata.create_all(db.engine)