#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, uuid

from transwarp.orm import Model, StringField, IntegerField, BooleanField, FloatField, TextField,TimestampField

class User(Model):
    __table__ = 'users'

    id = IntegerField(primary_key=True, auto_increment=True)
    name = StringField(size=50)
    email = StringField(updatable=False, size=50)
    password = StringField(50, default='123456')
    admin = BooleanField(default=False)
    image = StringField(500, default='')
    created_at = TimestampField(updatable=False, default=time.time)

class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, auto_increment=True, size=50)
    user_id = StringField(updatable=False, size=50)
    user_name = StringField(50)
    user_image = StringField(500)
    name = StringField(50)
    summary = StringField(200)
    content = TextField()
    created_at = TimestampField(updatable=False, default=time.time)

class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, auto_increment=True, size=50)
    blog_id = StringField(updatable=False, size=50)
    user_id = StringField(updatable=False, size=50)
    user_name = StringField(50)
    user_image = StringField(500)
    content = TextField()
    created_at = TimestampField(updatable=False, default=time.time)

