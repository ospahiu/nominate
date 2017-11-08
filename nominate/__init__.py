import os

from flask import Flask

app = Flask(__name__)
app.config.from_object("config")
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, app.config["DATABASE_NAME"]),
))
app.config.from_envvar('NOMINATE_SETTINGS', silent=True)

import nominate.views
