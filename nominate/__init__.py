import os

from flask import Flask

app = Flask(__name__)

# app.config.from_object(__name__)
# # Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'nominate.db'),
))
# app.config.from_envvar('NOMINATE_SETTINGS', silent=True)

import nominate.views
