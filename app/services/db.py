from flask_pymongo import PyMongo

#Init mongo database
mongo = PyMongo()

"""
method that calls the init of the DB
"""

def init_db(app):
    mongo.init_app(app)