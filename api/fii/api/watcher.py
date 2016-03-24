from flask import request, g
from flask_restful import Resource

from fii.models import Watcher
from fii.app import api
from fii.decorators import require


class WatcherResource(Resource):
    @require('email')
    def post(self):
        email = request.form['email']
        watcher, created = Watcher.get_or_create(g.store, {'email': email})
        if created:
            g.store.add(watcher)
            g.store.commit()

        return watcher.dict()


def register_watcher_resources():
    api.add_resource(WatcherResource, '/watcher')
