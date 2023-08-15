import os
from pathlib import Path

from flask import Flask
from adprovider import db


def secret_config(value):
    if (path := Path(value)).exists():
        return path.read_text()
    return value
###############################################################################
# Global Configuration
#
# WSGI app wrapper
dat = db.Datastore(
    secret_config(os.getenv('DATABASE_USER')),
    secret_config(os.getenv('DATABASE_PASS')),
    secret_config(os.getenv('DATABASE_HOST')),
    secret_config(os.getenv('DATABASE_NAME')),
)

app = Flask(__name__)

@app.route('/inform')
def inform():
    db.delay(dat)
    return 'success', 200
