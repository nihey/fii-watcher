from flask import g

from fii.app import app
from fii.api.watcher import register_watcher_resources
from fii.database import get_store

register_watcher_resources()


@app.before_request
def before_request():
    # Open na database connection
    g.store = get_store()


@app.after_request
def after_request(response):
    # Close database connection
    g.store.close()

    # Allow CORS
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST'
    return response
