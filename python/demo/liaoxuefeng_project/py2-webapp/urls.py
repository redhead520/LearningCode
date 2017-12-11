#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.web import get, post, patch, delete, ctx, getHTML,APIValueError, APIError, make_signed_cookie, interceptor
from models.allmodels import User, Blog, Comment
import re
import hashlib
from conf.config import configs
from apis import get_models_by_page
import json

_RE_MD5 = re.compile(r'^[a-zA-Z0-9_-]{6,32}$')
_RE_EMAIL =re.compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
_COOKIE_NAME = configs["cookie"]["sccretName"]
_COOKIE_KEY = configs["cookie"]["secretKey"]

@getHTML('/', 'blogs.html')
def index():
    print '>>>>>>>>>>>>>>>blog all'
    blogs = Blog.all()
    return dict(blogs=blogs, user=ctx.request.user)

@getHTML('/blog/(\d+)', 'blog_content.html')
def blog(id):
    blog = Blog.find_first(id=id)
    print blog
    print ctx.request.user
    return dict(blog=blog, user=ctx.request.user)

@getHTML('/register', 'register.html')
def register():
    return dict()

@getHTML('/login', 'login.html')
def login():
    return dict()

@getHTML('/manage/blogs','manage_blog_list.html')
def manage_blogs():
    # blogs, page = get_models_by_page(Blog, 1)
    return dict(page_index=1, user=ctx.request.user)

@getHTML('/manage/blogs/create','manage_blog_edit.html')
def create_blogs():
    print '1111111'*10
    # blogs, page = get_models_by_page(Blog, 1)
    # print blogs
    # print page
    return dict(action=u'新建日志', isedit=False,  user=ctx.request.user)

@getHTML('/manage/blogs/edit/(\d+)','manage_blog_edit.html')
def edit_blogs(id=0):
    print '2222222'*10
    blog = Blog.find_first(id=id)
    print blog['content']
    return dict(action=u'编辑日志',blog=blog, isedit=True, user=ctx.request.user)


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
    user = ctx.request.user
    print '注销==========>'
    print user
    print ctx.request.cookie
    if user:
        cookie, expires = make_signed_cookie(user['id'], user['password'], max_age=-10)
        ctx.response.set_cookie(_COOKIE_NAME, cookie, expires=expires)
    return user

@get('/api/blogs')
def api_get_blogs():
    page = ctx.request.params(page=1)
    blogs, page = get_models_by_page(Blog, page)
    print('get blogs:=====>{}'.format(len(blogs)))
    return dict(blogs=blogs, page=page.__dict__)

@post('/api/blogs')
def api_create_blog():
    i = ctx.request.input(name='', summary='', content='')
    name = i['name'].strip()
    summary = i['summary']
    content = i['content']
    if not name:
        raise APIValueError('name', 'name cannot be empty.')
    if not summary:
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content:
        raise APIValueError('content', 'content cannot be empty.')
    user = ctx.request.user
    print 'new blogs:=========>'
    blog = Blog(user_id=user['id'], user_name=user['name'],user_image=user['image'], name=name, summary=summary, content=content)
    print blog
    result = blog.save()
    return blog

@patch('/api/blogs')
def api_update_blog():
    i = ctx.request.input(id='', name='', summary='', content='')
    print '============update'
    id = i['id'].strip()
    name = i['name'].strip()
    summary = i['summary']
    content = i['content']
    if not id:
        raise APIValueError('id', 'id cannot be empty.')
    if not name:
        raise APIValueError('name', 'name cannot be empty.')
    if not summary:
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content:
        raise APIValueError('content', 'content cannot be empty.')
    user = ctx.request.user
    print 'update blogs:{}=========>'.format(id)
    blog = Blog(name=name, summary=summary, content=content)
    print blog
    result = blog.update(id=int(id))
    return blog

# 拦截器 优先级leve 0 (顶级)
@interceptor(level=0,startswith=['/manage','/api'], absolute=['/'], html=True)
def user_interceptor(next):
    if hasattr(ctx.request, 'user_id') and ctx.request.user == None:
        user = User.find_first(id=ctx.request.user_id)
        if user:
            md5 = hashlib.md5('%s-%s-%s-%s' % (ctx.request.user_id, user['password'], ctx.request.expires, _COOKIE_KEY)).hexdigest()
            if md5 == ctx.request.cookie_md5:
                ctx.request.user = user
    return next()

@interceptor()
def mange_interceptor(next):
    user = ctx.request.user
    route = ctx.request.path
    if user != None and route.startswith('/manage'):
        if not user['admin']:
            # redirect()
            pass
    return next()