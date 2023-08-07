from random import randint
from time import sleep

from faker import Faker
from flask import Flask, request

###############################################################################
# Global Configuration
#
# WSGI app wrapper
app = Flask(__name__)

@app.before_request
def before_request():
    sleep(randint(1, 5))

@app.route('/serve')
def user():
    if request.args.get('raise'):
        raise ConnectionError('cannot connect to the ad server database')
    
    return Faker().json(data_columns=[
        ('adProvider', 'company'), 
        ('id', 'pyint'), 
        ('content', 'paragraph', {'nb_sentences': 5})
    ], num_rows=1)
