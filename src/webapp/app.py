import os
from collections import namedtuple
from pathlib import Path

import requests as req

from flask import (
    Flask, 
    render_template
)
from opentelemetry import( 
    metrics, 
    trace
)
from webapp import db


def secret_config(value):
    if (path := Path(value)).exists():
        return path.read_text()
    return value
###############################################################################
# Global Configuration
#
exception_counter = metrics.get_meter("exceptions.meter").create_counter(
    name="exceptions", 
    description="number of exceptions caught", 
    value_type=int
)

ads_req_counter = metrics.get_meter("ads.requested").create_counter(
    name="ads_requested",
    description="number of requested ads",
    value_type=int
)

ads_rec_counter = metrics.get_meter("ads.recieved").create_counter(                                
    name="ads_requested",
    description="number of requested ads",
    value_type=int
)


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


@app.errorhandler(Exception)
def handle_bad_request(e):
    exception_counter.add(1, exception_type=type(e))
    return 'something went wrong, reload and try again.', 500

@app.route('/')
def index():
    try:
        ads_req_counter.add(1)
        adverts = req.get(f'http://{ads.host}:{ads.port}{ads.path}').json()
        ads_rec_counter.add(1)
    except Exception as ex:
        adverts = {}
        exception_counter.add(1, exception_type=type(ex))
    
    return render_template('index.html', 
        records=db.timeline(dat),
        adverts=adverts,
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
        
