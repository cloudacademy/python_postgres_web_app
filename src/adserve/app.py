from random import randint
from time import sleep

from faker import Faker
from flask import Flask

###############################################################################
# Global Configuration
#
# WSGI app wrapper
app = Flask(__name__)


# Accept a username and return customized ads
@app.route('/serve')
def user():
    sleep(randint(1, 5))
    
    return Faker().json(data_columns=[
        ('adProvider', 'company'), 
        ('id', 'pyint'), 
        ('content', 'paragraph', {'nb_sentences': 5})
    ], num_rows=1)
