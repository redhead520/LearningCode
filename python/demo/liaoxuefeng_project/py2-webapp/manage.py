#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector

from transwarp import db
from models.allmodels import User

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

b = User(id=3, name='55555',email='5555@wwerf.com')
c = User(id=5, name='cccc',email='cccc@wwerf.com')
# print b.save()
# with db.connection():
#   print User.select(id=3)
#   print User.select(id=4)
#   print User.select(id=5)

print '-'*10
print c.update(id=3)
# with db.transaction():
#     print c.update(id=3)
#     print User.select(id=3)
#     print User.delete(id=3)

# a = User(id=9, name='df93',email='9999@wwerf.com')
#
# r = a.save()
# print r
# # a.save()
# r = a.update()
# print r
# result = User.select(id=9)
# print result
# print '-'*20
# result = User.delete(id=9)
# print result