#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for

from peewee import *

LIST_DB = SqliteDatabase('listitems.db')

app = Flask(__name__)

app.config['SECRET_KEY'] = '876H87^H685f&6f5ryh7EDHg74g63s'

# define a list item class
class ListItem(Model):
  
@app.route('/add', methods=['POST'])
def add_item():
    ''' add items to the list '''
    return "stub"

@app.route('/view')
def view_items():
    ''' view items in the list '''
    return "stub"

@app.route('/delete/<this_id>')
def delete_item(this_id):
    ''' delete items from the list '''
    return "stub"

@app.route('/strike/<this_id>')
def strike(this_id):
    ''' move items to and from deletion staging area '''

@app.route('/')
def home():
    ''' applicaiton root '''
    return "stub"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)