import os

from flask import Flask
from flask_login import LoginManager

from nominate.tasks import make_celery

app = Flask(__name__)
app.config.from_object("config")
# Load default config and override config from an environment variable.
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, app.config["DATABASE_NAME"]),
))
app.config.from_envvar('NOMINATE_SETTINGS', silent=True)
app.jinja_env.globals.update(len=len)
app.jinja_env.globals.update(range=range)
app.jinja_env.globals.update(int=int)
login_manager = LoginManager()
login_manager.init_app(app)
celery = make_celery(app)

import nominate.views
