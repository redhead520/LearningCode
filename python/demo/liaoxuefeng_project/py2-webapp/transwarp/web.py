#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import functools
import logging
from cgi import escape
from urlparse import parse_qs
import json
import exceptions
import os
from conf.config import configs
import datetime, time

# 定义MIME类型
MIME = {
    '.js': 'application/x-javascript',
    '.css': 'text/css',
    '.html': 'text/html',
    '.jpeg': 'image/jpeg',
    '.ico': 'application/x-ico',
    '.svg': 'image/svg+xml',
    '.otf': 'application/octet-stream',
    '.eot': 'application/octet-stream',
    '.ttf': 'application/octet-stream',
    '.woff': 'application/x-font-woff',
    '.woff2': 'application/x-font-woff',
}
#                  )
# 全局ThreadLocal对象：
ctx = threading.local()

# HTTP错误类:
class HttpError(Exception):
    pass

# request对象:
class Request(object):
    # 根据key返回value:
    def __init__(self, env):
        self.env = env
        try:
            request_body_size = int(env.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = env['wsgi.input'].read(request_body_size)
        params = parse_qs(env['QUERY_STRING'])
        data = parse_qs(request_body)

        # 转义，防止脚本注入
        for k, v in params.items():
            params[k] = escape(v[0])
        for k, v in data.items():
            data[k] = escape(v[0])
        # print '**'*20
        # for k,v in env.items():
        #     print k, ':', v
        self.params = params
        self.data = data
        self.path = env['PATH_INFO']
        self.method = env['REQUEST_METHOD']
        self.content_type = env['CONTENT_TYPE']
        self.http_accept = env['HTTP_ACCEPT']
        self.handle_name = '{}{}'.format(self.method, self.path).lower()

    def get(self, key, default=None):
        return self.params.get(key, default)

    # 返回key-value的dict:
    def input(self):
        return self.data

    # 返回URL的path:
    @property
    def path_info(self):
        return self.path

    # 返回HTTP Headers:
    @property
    def headers(self):
        pass

    # 根据key返回Cookie value:
    def cookie(self, name, default=None):
        pass
    def __str__(self):
        return '(Request: {})'.format(self.__dict__)

# response对象:
class Response(object):
    # 设置header:
    def __init__(self):
        self.__status = '200 OK'
        self.headers = {
            'Content-Type': 'application/json'
        }

    def set_header(self, key, value):
        self.headers[key] = value

    # 设置Cookie:
    def set_cookie(self, name, value, max_age=None, expires=None, path='/'):
        pass

    # 设置status:
    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, value):
        try:
          self.__status = int(value)
        except:
            pass

# 中间件
class Beforeware:
    def __init__(self, app):
        self.wrapped_app = app
    def __call__(self, environ, start_response):

        ctx.request = Request(environ)
        ctx.response = Response()

        for data in self.wrapped_app(environ, start_response):
            if ctx.response.headers['Content-Type'] == 'application/json':
                data = json.dumps(data)
            yield data

def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

# 定义GET:
def get(path):
    '''
        Define decorator @get('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator

# 定义POST:
def post(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper

    return decorator

# 处理静态资源
def staticFileRoute(path):
    try:
        ctx.response.headers['Content-Type'] = MIME[os.path.splitext(path)[1]]
    except:
        ctx.response.headers['Content-Type'] = ctx.request.content_type
    static_path = os.path.join(configs['www'],path.lstrip('/'))
    print '+'*20
    try:
        with open(static_path) as f:
            data = f.read()
    except:
        data = ''

    return data

# 定义模板:
def view(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            ctx.response.headers['Content-Type'] = 'text/html'
            data = func(*args, **kw)
            return WSGIApplication.template_engine(path, data)
        return wrapper

    return decorator

# 定义拦截器:
def interceptor(pattern):
    pass

# 定义模板引擎:
class TemplateEngine(object):
    def __call__(self, path, model):
        pass

# 缺省使用jinja2:
class Jinja2TemplateEngine(TemplateEngine):
    def __init__(self, templ_dir, **kw):
        from jinja2 import Environment, FileSystemLoader
        self._env = Environment(loader=FileSystemLoader(templ_dir), **kw)

    def __call__(self, path, model):
        return self._env.get_template(path).render(**model).encode('utf-8')

    def add_filter(self, name, filter_fn):
        self._env.filters[name] = filter_fn


# WSGI
class WSGIApplication(object):
    template_engine = None
    def __init__(self, document_root=None, **kw):
        self.urls = {}

    # 添加一个URL定义:
    def add_url(self, func):
        key = '{}{}'.format(func.__method__, func.__route__).lower()
        if not self.urls.has_key(key):
            self.urls[key] = func
        else:
            raise exceptions.StandardError('regist url functions error')
    # 添加URL模块:
    def add_module(self, urls):
        for i in dir(urls):
            try:
                func = getattr(urls,i)
                if hasattr(func, '__route__'):
                    self.add_url(func)
            except:
                pass

    # 添加一个Interceptor定义:
    def add_interceptor(self, func):
        pass

    # 设置TemplateEngine:

    @property
    @classmethod
    def template_engine(cls):
        return cls._template_engine

    @template_engine.setter
    @classmethod
    def template_engine(cls, engine=None):
        if engine:
            ctx.template_engine = engine
            cls._template_engine = engine


# WSGI application
    # 返回WSGI处理函数:
    def get_wsgi_application(self):
        def wsgi(env, start_response):
            handle_func = self.urls.get(ctx.request.handle_name)
            # urls定义过的route访问
            if handle_func:
                body = handle_func()
            # 网站资源访问（www目录）
            elif ctx.request.method == 'GET':
                body = staticFileRoute(ctx.request.path)
            start_response(ctx.response.status, ctx.response.headers.items())
            return [body]
        return wsgi
#WSGI server
    # 开发模式下直接启动WSGI服务器:
    def run(self, port=9000, host='127.0.0.1'):
        from wsgiref.simple_server import make_server
        server = make_server(host, port, Beforeware(self.get_wsgi_application()))
        print('run server on {}:{}'.format(host, port))
        server.serve_forever()
        # server.handle_request() # 只能处理一次请求