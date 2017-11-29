#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector

from transwarp import db
from models.user import User
db_config = {
    'user':'root',
    'password':'0311020045',
    'database':'mysql',
    'host':'162.219.127.17',
    'port':3306
}
# sql = 'select user, host, authentication_string from user'
# db.create_engine(**db_config)
# users = db.select(sql)
# print('结果：')
# print '-'*20auto_increment
# print users
# for i in users:
#     print(i)

a = User(id=3, name='color')
print a
for k, v in a.__mappings__.items():
    print k
    print v.__dict__
    print '-'*5
# a.save()
# a.update()
# b = User()
# b.select(id=4)