from flask import Flask
from flask.ext.restful import Api
from werkzeug.utils import ImportStringError

app = Flask(__name__)

app.config.from_object('fii.config.Config')
try:
    app.config.from_object('fii.localconfig.Config')
except ImportStringError:
    pass

api = Api(app, prefix='/api')
