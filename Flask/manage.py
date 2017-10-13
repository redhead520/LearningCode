#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask_script import Manager
from app import app
from models import messages
import json
import sqlite3

manager = Manager(app)

@manager.command
def new():
    message = messages(None, 'getposition', 'id=222', '2017-09-30', 'False')
    r = message.save()
    print r

@manager.option('-m', '--msg', dest='msg_val', default='world')
def hello_world(msg_val):
    print 'hello ' + msg_val

@manager.command
def init_db():
    messages.init()
    print 'init db complete!!'

@manager.command
def query():
    print '*'*50
    print messages.query()
    print 'init db complete!!'

if __name__ == "__main__":
    manager.run()