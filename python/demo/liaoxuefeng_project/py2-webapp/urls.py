#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.web import get, post, ctx, getHTML,APIValueError, APIError
from models.allmodels import User, Blog, Comment
import re
import hashlib
import time

_RE_MD5 = re.compile(r'^[a-zA-Z0-9_-]{6,32}$')
_RE_EMAIL =re.compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
_COOKIE_NAME = 'test_cookie_name'
_COOKIE_KEY = 'test_cookie_key'

@getHTML('/', 'blogs.html')
def index():
    blogs = Blog.all()
    user = User.all()[0]
    # ctx.response.content_type = 'text/html'
    return dict(blogs=blogs, user=user)

@getHTML('/register', 'register.html')
def index():
    return dict()

@get('/home')
def home():
    # ctx.response.content_type = 'text/json'
    # ctx.response.set_cookie('name', 'value', expires=3600)
    return 'hello huang hongfa'

@get('/api/users')
def api_get_users():
    users = User.all()
    # 把用户的口令隐藏掉:
    for u in users:
        u['password'] = '******'
    return dict(users=users)


@post('/api/users')
def register_user():
    i = ctx.request.input(name='', email='', password='')
    name = i['name'].strip()
    email = i['email'].strip().lower()
    password = i['password']
    if not name:
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_MD5.match(password):
        raise APIValueError('password')
    user = User.find_first(email=email)
    if user:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    user = User(name=name, email=email, password=password,
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email).hexdigest())
    user.save()
    return user

@post('/api/authenticate')
def authenticate():
    i = ctx.request.input(email='', password='')
    email = i['email'].strip().lower()
    password = i['password']
    user = User.find_first(email=email)
    if user is None:
        raise APIError('auth:failed', 'email', 'Invalid email.')
    elif user['password'] != password:
        raise APIError('auth:failed', 'password', 'Invalid password.')
    max_age = 604800
    cookie = make_signed_cookie(user['id'], user['password'], max_age)

    ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)

    return user

# 计算加密cookie:
def make_signed_cookie(id, password, max_age):
    expires = str(int(time.time() + max_age))
    L = [id, expires, hashlib.md5('%s-%s-%s-%s' % (id, password, expires, _COOKIE_KEY)).hexdigest()]
    return '-'.join(L)