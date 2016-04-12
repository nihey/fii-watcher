from flask import request, g
from flask_restful import Resource

from fii.models import Watcher, FII
from fii.app import api
from fii.decorators import require
from fii.utils import error_message


class WatcherResource(Resource):
    @require('email')
    def post(self):
        email = request.form['email']
        watcher, created = Watcher.get_or_create(g.store, {'email': email})
        if created:
            g.store.add(watcher)
            g.store.commit()

        return watcher.dict()


class FIIResource(Resource):
    def get(self):
        return [f.dict() for f in g.store.query(FII)]

    @require('email', 'code')
    def post(self):
        # Check if the FII really exists
        code = request.form['code']
        fii = g.store.query(FII).filter(FII.code == code).first()
        if fii is None:
            return error_message(404, 'fii_not_found')

        email = request.form['email']
        # Add watcher and establish the relation with the FII
        watcher, created = Watcher.get_or_create(g.store, {'email': email})
        if created:
            g.store.add(watcher)
        fii.watchers.append(watcher)
        g.store.commit()

        # Return both values
        return watcher.dict()


def register_watcher_resources():
    api.add_resource(WatcherResource, '/watcher')
    api.add_resource(FIIResource, '/fii')
