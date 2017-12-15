#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.web import get, post, patch,WSGIApplication, delete, ctx, getHTML,APIValueError, APIError, make_signed_cookie, interceptor
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
    # print '>>>>>>>>gg>>blog all'
    blogs = Blog.all()
    return dict(blogs=blogs, user=ctx.request.user)

@getHTML('/blog/(\d+)', 'blog_content.html')
def blog(id):
    blog = Blog.find_first(id=id)
    # print blog
    # print ctx.request.user
    return dict(blog=blog, user=ctx.request.user)

@getHTML('/register', 'register.html')
def register():
    return dict()

@getHTML('/login', 'login.html')
def login():
    return dict()

@getHTML('/manage/users','manage_users_list.html')
def manage_users():
    return dict(page_index=1, user=ctx.request.user)

@getHTML('/manage/comments','manage_comments_list.html')
def manage_comments():
    return dict(page_index=1, user=ctx.request.user)

@getHTML('/manage/blogs','manage_blog_list.html')
def manage_blogs():
    return dict(page_index=1, user=ctx.request.user)

@getHTML('/manage/blogs/create','manage_blog_create.html')
def create_blogs():
    return dict(action=u'新建日志', isedit=False,  user=ctx.request.user)

@getHTML('/manage/blogs/edit/(\d+)','manage_blog_edit.html')
def edit_blogs(id=0):
    blog = Blog.find_first(id=id)
    return dict(action=u'编辑日志',blog=blog, isedit=True, user=ctx.request.user)


@get('/api/users')
def api_get_users():

    page = ctx.request.params(page=1)
    user = ctx.request.user
    where = None
    users, page = get_models_by_page(User, page, where=where)
    # 把用户的口令隐藏掉:
    for u in users:
        u['password'] = '******'
    # print('get users:=====>{}'.format(len(users)))
    return dict(users=users, page=page.__dict__)

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
    # print '注销==========>'
    # print user
    # print ctx.request.cookie
    if user:
        cookie, expires = make_signed_cookie(user['id'], user['password'], max_age=-10)
        ctx.response.set_cookie(_COOKIE_NAME, cookie, expires=expires)
    return user

@get('/api/blogs')
def api_get_blogs():
    page = ctx.request.params(page=1)
    user = ctx.request.user
    where = None
    if not user['admin']:
        where = {'user_id':user['id']}
    blogs, page = get_models_by_page(Blog, page,where=where)
    # print('get blogs:=====>{}'.format(len(blogs)))
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
    # print 'new blogs:=========>'
    blog = Blog(user_id=user['id'], user_name=user['name'],user_image=user['image'], name=name, summary=summary, content=content)
    # print blog
    result = blog.save()
    return blog

@patch('/api/blogs')
def api_update_blog():
    # print '>>>>>>>> update blogs'
    i = ctx.request.input()
    id = i['id']
    name = i['name']
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
    print 'update blog:{}=========>'.format(id)
    blog = Blog(name=name, summary=summary,content=content)
    result = blog.update(id=int(id))
    return blog

@delete('/api/blogs')
def api_delete_blog():
    i = ctx.request.params(id='')
    id = i['id']
    print 'delete blog:{}=========>'.format(id)
    print i
    if not id:
        raise APIValueError('id')
    result = Blog.delete(id=int(id))
    return result

@get('/api/comments')
def api_get_comments():
    page = ctx.request.params(page=1)
    user = ctx.request.user
    where = None
    Comments, page = get_models_by_page(Comment, page,where=where)
    print('get blogs:=====>{}'.format(len(Comments)))
    return dict(Comments=Comments, page=page.__dict__)

@post('/api/comments')
def api_create_comment():
    i = ctx.request.input()
    user = ctx.request.user
    blog_id = i['blog_id']
    content = i['content']
    if not blog_id:
        raise APIValueError('blog_id', 'blog_id cannot be empty.')
    if not content:
        raise APIValueError('content', 'content cannot be empty.')
    if not user:
        raise APIValueError('user', 'user cannot be empty.please login in!')

    print 'new comments:=========>'
    comment = Comment(
        user_id=user['id'],
        user_name=user['name'],
        user_image=user['image'],
        blog_id=blog_id,
        content=content)
    print comment
    result = comment.save()
    return comment

@delete('/api/comments')
def api_delete_comment():
    i = ctx.request.input(id='')
    id = i['id']
    if not id:
        raise APIValueError('id', 'id cannot be empty.')
    user = ctx.request.user
    print 'delete comment:{}=========>'.format(id)
    result = Comment.delete(id=int(id))
    return result


# 拦截器 优先级leve 0 (顶级)
@interceptor(level=0,startswith=['/manage','/api'], absolute=['/'], html=True)
def user_interceptor(next):
    if hasattr(ctx.request, 'user_id') and ctx.request.user == None:
        user = User.find_first(id=ctx.request.user_id)
        if user:
            md5 = hashlib.md5('%s-%s-%s-%s' % (ctx.request.user_id, user['password'], ctx.request.expires, _COOKIE_KEY)).hexdigest()
            if md5 == ctx.request.cookie_md5:
                print 'manage page add user:{}'.format(user['name'])
                ctx.request.user = user
    return next()

@interceptor(level=9,startswith=['/manage'], html=True)
def mange_interceptor(next):
    user = ctx.request.user
    if user == None:
        body = WSGIApplication.redirect('/login')
        return [ body ]
    return next()