#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.web import get, post, delete, ctx, getHTML,APIValueError, APIError, make_signed_cookie, interceptor
from models.allmodels import User, Blog, Comment
import re
import hashlib
from conf.config import configs

_RE_MD5 = re.compile(r'^[a-zA-Z0-9_-]{6,32}$')
_RE_EMAIL =re.compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
_COOKIE_NAME = configs["cookie"]["sccretName"]
_COOKIE_KEY = configs["cookie"]["secretKey"]

@getHTML('/', 'blogs.html')
def index():
    blogs = Blog.all()
    user = User.all()[0]
    user = ctx.request.user
    # ctx.response.content_type = 'text/html'
    return dict(blogs=blogs, user=user)

@getHTML('/register', 'register.html')
def register():
    return dict()

@getHTML('/login', 'login.html')
def login():
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

# 注册
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
    if not password:
        raise APIValueError('password')
    user = User.find_first(email=email)
    if user:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    user = User(name=name, email=email, password=password,
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email).hexdigest())
    result = user.save()
    if result == None:
        result = User.find_first(email=email)
        result['password'] = '*******'
    return result

# 登录
@post('/api/authenticate')
def loginin():
    i = ctx.request.input(email='', password='')
    email = i['email'].strip().lower()
    password = i['password']
    print '登录'
    print email
    print password
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email', 'Invalid email.')
    if not password or not _RE_MD5.match(password):
        raise APIValueError('passwd', 'Invalid password.')
    user = User.find_first(email=email)
    if user is None:
        raise APIError('auth:failed', 'email', 'Email not exist.')
    # check password 不加密不加盐
    if user['password'] != password:
        raise APIError('auth:failed', 'password', 'Invalid password.')
    cookie, expires = make_signed_cookie(user['id'], user['password'])
    ctx.response.set_cookie(_COOKIE_NAME, cookie, expires=expires)
    return user

# 注销
@delete('/api/authenticate')
def loginout():
    cookie = ';'
    ctx.response.set_cookie(cookie, expires=0)



@interceptor('/')
def user_interceptor(next):
    if hasattr(ctx.request, 'user_id'):
        user = User.find_first(id=ctx.request.user_id)
        if user:
            md5 = hashlib.md5('%s-%s-%s-%s' % (ctx.request.user_id, user['password'], ctx.request.expires, _COOKIE_KEY)).hexdigest()
            if md5 == ctx.request.cookie_md5:
                ctx.request.user = user
    return next()