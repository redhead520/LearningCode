#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.web import get, post, ctx, view
from models.allmodels import User, Blog, Comment


@view('blogs.html')
@get('/')
def index():
    blogs = Blog.all()
    user = User.all()[0]
    # ctx.response.content_type = 'text/html'
    return dict(blogs=blogs, user=user)

@get('/home')
def home():
    # ctx.response.content_type = 'text/json'
    # ctx.response.set_cookie('name', 'value', expires=3600)
    return 'hello huang hongfa'

# wsgi.add_url(test)
# wsgi.add_url(home)