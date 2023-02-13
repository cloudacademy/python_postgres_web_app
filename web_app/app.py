import os
import db
from flask import Flask, render_template

###############################################################################
# Global Configuration
#
# WSGI app wrapper
app = Flask(__name__)
# Database engine wrapper
dat = db.Datastore(
    os.getenv('DATABASE_USER'),
    os.getenv('DATABASE_PASS'),
    os.getenv('DATABASE_HOST'),
    os.getenv('DATABASE_NAME'),
)


@app.route('/')
def index():
    return 'Welcome to Overshare! Yet another social media app.  Click <a href="/timeline">here</a> to view the timeline.'

@app.route('/timeline')
def timeline():
    try:
        return render_template('index.html', records=db.get_timeline(dat))
    except:
        return 'Is the database up and running?', 500

if __name__ == '__main__':
    db.init(dat)
    db.populate_db(dat)