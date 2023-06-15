import os
import db
from flask import Flask, render_template
from pathlib import Path

###############################################################################
# Determines if the value is a file path or a string
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
    os.getenv('DATABASE_HOST'),
    os.getenv('DATABASE_NAME'),
)


@app.route('/')
def index():
    return """
    Welcome to Overshare! Yet another social media app.  
    
    Click <a href="/timeline">here</a> to view the timeline.

    Promotion: 50% off on all Overshare merchandise! Use code "OVERSHARE" at checkout.

    """

@app.route('/timeline')
def timeline():
    try:
        return render_template('index.html', records=db.get_timeline(dat))
    except:
        return 'Is the database up and running?', 500

if __name__ == '__main__':
    db.init(dat)
    db.populate_db(dat)