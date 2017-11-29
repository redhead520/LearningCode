#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transwarp.orm import Model, IntegerField, StringField

class User(Model):
    __table__ = 'users'

    id = IntegerField(primary_key=True)
    name = StringField(50)
    note = StringField(default='no things')


