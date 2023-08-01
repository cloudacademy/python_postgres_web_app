import os
from pathlib import Path
from collections import namedtuple

from webapp import db
from flask import Flask, render_template
import requests as req

def secret_config(value):
    if (path := Path(value)).exists():
        return path.read_text()
    return value
###############################################################################
# Global Configuration
#
# WSGI app wrapper
app = Flask(__name__)
# Database engine wrapper
dat = db.Datastore(
    secret_config(os.getenv('DATABASE_USER')),
    secret_config(os.getenv('DATABASE_PASS')),
    secret_config(os.getenv('DATABASE_HOST')),
    secret_config(os.getenv('DATABASE_NAME')),
)

ads = namedtuple('ads', ['host', 'port', 'path'])
ads.host = os.getenv('ADSERVE_HOST')
ads.port = os.getenv('ADSERVE_PORT')
ads.path = os.getenv('ADSERVE_PATH')

@app.route('/')
def index():
    return render_template('index.html', 
        records=db.timeline(dat),
        adverts=req.get(f'http://{ads.host}:{ads.port}{ads.path}').json(),
    )

# Route for the user profile page
@app.route('/user/<username>')
def user(username):
    return render_template('user_detail.html', 
        details=db.user_detail_summary(dat, username),
        records=db.user_posts(dat, username),
    )

if __name__ == '__main__':
    try:
        db.init(dat)
        db.populate_db(dat)
    except Exception as ex:
        pass
        
