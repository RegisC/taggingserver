from app.config import Config
import flask

instance = flask.Flask(__name__)
instance.config.from_object(Config)

from app import routes
