import os
from collections import namedtuple
from random import randint
from time import sleep

from faker import Faker
from flask import Flask, request

import requests as req
###############################################################################
# Global Configuration
#
# WSGI app wrapper
app = Flask(__name__)

prov = namedtuple('ads', ['host', 'port', 'path'])
prov.host = os.getenv('PROVIDER_HOST')
prov.port = os.getenv('PROVIDER_PORT')
prov.path = os.getenv('PROVIDER_PATH')

@app.before_request
def before_request():
    sleep(randint(1, 5))

@app.route('/serve')
def user():
    if request.args.get('raise'):
        raise ConnectionError('cannot connect to the ad server database')

    ad = Faker().json(data_columns=[
        ('adProvider', 'company'), 
        ('id', 'pyint'), 
        ('content', 'paragraph', {'nb_sentences': 5})
    ], num_rows=1)

    # inform the provider that the ad was successful.
    req.get(f'http://{prov.host}:{prov.port}{prov.path}')
    
    return ad

