#!/usr/bin/env python
import os, urlparse
from flask import Flask, render_template, request, redirect, url_for

from peewee import *

urlparse.uses_netloc.append('postgres')
db_url = urlparse.urlparse(os.environ['DATABASE_URL'])

# for your config
DATABASE = {
    'engine': 'peewee.PostgresqlDatabase',
    'name': db_url.path[1:],
    'password': db_url.password,
    'host': db_url.hostname,
    'port': db_url.port,
}

app = Flask(__name__, instance_relative_config=True)
LIST_DB = PostgresqlDatabase(DATABASE)

# create a settings.cfg in the base directory with the uncommented line:
# SECRET_KEY = 'yourGibberishStringHere'
app.config.from_pyfile('settings.cfg', silent=True)

# define a list item class
class ListItem(Model):
    content = CharField()
    strike = BooleanField(default=False)
    
    class Meta:
        database = LIST_DB

def initialize():
    ''' initialize the DB if needed '''
    LIST_DB.connect()
    LIST_DB.create_tables([ListItem], safe=True)

@app.route('/add', methods=['POST'])
def add_item():
    ''' add items to the list '''
    ListItem.create(content=request.form['contentadd'])
    return redirect(url_for('view_items'))

@app.route('/view')
def view_items():
    ''' view items in the list '''
    items = ListItem.select()
    if items:
        return render_template('view.html', items=items)
    else:
        print("No items")

@app.route('/delete/<this_id>')
def delete_item(this_id):
    ''' delete items from the list '''
    q = ListItem.delete().where(ListItem.id == this_id)
    q.execute()
    return redirect(url_for('view_items'))

@app.route('/strike/<this_id>')
def strike(this_id):
    ''' move items to and from deletion staging area '''
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
    ''' application root '''
    return redirect(url_for('view_items'))

if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', port=5000)