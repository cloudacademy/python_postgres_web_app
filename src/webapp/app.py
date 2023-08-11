import os
from collections import namedtuple
from pathlib import Path

import requests as req

from faker import Faker

from flask import (
    Flask, 
    render_template,
    request
)
from opentelemetry import( 
    metrics
)
from webapp import db
from webapp.jobs import Jobs, translate_post

def secret_config(value):
    if (path := Path(value)).exists():
        return path.read_text()
    return value
###############################################################################
# Global Configuration
#
exception_counter = metrics.get_meter("exception.meter").create_counter(
    name="exceptions", 
    description="number of exceptions caught"
)

ads_req_counter = metrics.get_meter("ads.requested").create_counter(
    name="ads_requested",
    description="number of requested ads"
)

ads_rec_counter = metrics.get_meter("ads.recieved").create_counter(                                
    name="ads_requested",
    description="number of requested ads"
)


# Post translation jobs
jobs = Jobs()
jobs.start()

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
    exception_counter.add(1, { 'exception_type': str(type(e)) })
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


# The following route is used to create a new post
@app.route('/post', methods=['POST'])
def post():
    print(f'creating post: {request.form}')
    db.post(dat, request.form['title'], request.form['user_id'], request.form['content'])
    # Enqueue the translation job.
    jobs.enqueue(translate_post, request.form['content'])
    return 'success', 200



import atexit
@atexit.register
def shutdown():
    jobs.stop()

if __name__ == '__main__':
    try:
        import psycopg #imported to use the exception below.
        db.init(dat)
    except:
        pass
        
    try:
        db.populate_db(dat)
        
        fake = Faker(['ja_JP']) 
        # uses the standard library to post to the /post endpoint. 
        # loops 100 times, once for each user. Uses the faker library to generate fake data.
        for n in range(1, 100):
            app.test_client().post("/post", data={ 'title': fake.sentence(), 'user_id': n, 'content': fake.text() })

    except Exception as ex:
        print(ex)
        
        
