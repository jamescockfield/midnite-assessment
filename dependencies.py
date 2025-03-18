from flask_injector import FlaskInjector, singleton
from repositories import UserActivityRepository
from services import AlertBuilder
from database.database import db

def configure(binder):
    repository = UserActivityRepository(db.session)

    binder.bind(UserActivityRepository, to=repository, scope=singleton)
    binder.bind(AlertBuilder, to=AlertBuilder(repository), scope=singleton)

def init_dependencies(app):
    FlaskInjector(app=app, modules=[configure]) 