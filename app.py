#!/usr/bin/env python
import os
import urlparse
import psycopg2
from flask_debugtoolbar import DebugToolbarExtension

from flask import Flask, render_template, request, redirect, url_for
from peewee import *

# Set up DB
if 'HEROKU' in os.environ:
    DEBUG=False
    APP_PORT=5000
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    DATABASE = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': url.path[1:],
        'user': url.username,
        'password': url.password,
        'host': url.hostname,
        'port': url.port,
        }
    LIST_DB = PostgresqlDatabase(DATABASE['name'], host=DATABASE['host'], port=DATABASE['port'], user=DATABASE['user'], password=DATABASE['password'])
else:
    DEBUG=True
    APP_PORT=8080
    LIST_DB = SqliteDatabase('listitem.db')

app = Flask(__name__)

# create a settings.cfg in the base directory with the uncommented line:
# SECRET_KEY = 'yourGibberishStringHere'
app.config.from_pyfile('settings.cfg', silent=True)
app.debug = DEBUG
toolbar = DebugToolbarExtension(app)

# define a list item class
class ListItem(Model):
    content = CharField()
    strike = BooleanField(default=False)
    todo = CharField()
    
    class Meta:
        database = LIST_DB

def initialize():
    """Initialize the DB safely."""
    LIST_DB.connect()
    LIST_DB.create_tables([ListItem], safe=True)
    LIST_DB.close()

@app.before_request
def before_request():
    """Connect to the database before each request."""
    LIST_DB.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    LIST_DB.close()
    return response

@app.route('/add', methods=['POST'])
def add_item():
    """Add items to the list."""
    try:
        ListItem.create(content=request.form['contentadd'], todo=request.form['itemtype'])
    except:
        ListItem.create(content=request.form['contentadd'], todo="off")
    return redirect(url_for('view_items'))

@app.route('/view')
def view_items():
    """View items in the list."""
    items = ListItem.select()
    if items:
        return render_template('view.html', items=items)
    else:
        print("No items")

@app.route('/delete/<this_id>')
def delete_item(this_id):
    """Delete items from the list."""
    q = ListItem.delete().where(ListItem.id == this_id)
    q.execute()
    return redirect(url_for('view_items'))

@app.route('/strike/<this_id>')
def strike(this_id):
    """Move items to and from deletion staging area."""
    rec = ListItem.get(ListItem.id == this_id)
    if rec.strike:
      q = ListItem.update(strike=False).where(ListItem.id == this_id)
      q.execute()
    else:
      q = ListItem.update(strike=True).where(ListItem.id == this_id)
      q.execute()
    return redirect(url_for('view_items'))

@app.route('/')
def home():
    """Application root."""
    return redirect(url_for('view_items'))

if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', port=APP_PORT)