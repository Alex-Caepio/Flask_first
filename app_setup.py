import psycopg2
from flask import Flask

app = Flask(__name__)
app.debug = True

conn = psycopg2.connect(dbname='travellist', user='travellist_user', password='password', host='172.20.0.3')
