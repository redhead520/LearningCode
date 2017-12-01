#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector

from transwarp import db
from models.allmodels import User
from transwarp.web import *

# import logging
# # level: CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(process)d %(thread)d %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                  )
db_config = {
    'user':'root',
    'password':'0311020045',
    'database':'awesome',
    'host':'162.219.127.17',
    'port':3306
}
db.create_engine(**db_config)

wsgi = WSGIApplication()

@get('/')
def test():
    input_data = ctx.request.input()
    ctx.response.content_type = 'text/plain'
    ctx.response.set_cookie('name', 'value', expires=3600)
    return 'result'

@get('/home')
def home():
    ctx.response.content_type = 'text/plain'
    ctx.response.set_cookie('name', 'value', expires=3600)
    return 'hello huang hongfa'

wsgi.add_url(test)
wsgi.add_url(home)

if __name__ == '__main__':
    # 开发模式（Development Mode）
    wsgi.run()
else:
    # 产品模式（Production Mode）
    application = wsgi.get_wsgi_application()