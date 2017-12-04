#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.web import get, post, ctx, view
from models.allmodels import User


# @view('test_users.html')
@get('/')
def test_users():
    print '000'
    users = User.all()
    # ctx.response.content_type = 'text/html'
    return users

@get('/home')
def home():
    # ctx.response.content_type = 'text/json'
    # ctx.response.set_cookie('name', 'value', expires=3600)
    return 'hello huang hongfa'

# wsgi.add_url(test)
# wsgi.add_url(home)