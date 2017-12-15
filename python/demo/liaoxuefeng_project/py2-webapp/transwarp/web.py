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
import re
import hashlib
from models.allmodels import User

_COOKIE_NAME = configs["cookie"]["sccretName"]
_COOKIE_KEY = configs["cookie"]["secretKey"]
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

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
def HttpError(Exception):
    return exceptions

def APIError(*args):
    return exceptions.ValueError('{}'.format(str(args)))

def APIValueError(value):
    return exceptions.ValueError('you input value({}) was wrong!'.format(value))

def getParameter(s):
    r = re.findall(r'name="(.*?)"\r\n\r\n(.*?)\r\n', s, re.S)
    return dict(r) if r else parse_qs(s)

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
        data = getParameter(request_body)
        # 转义，防止脚本注入
        for k, v in params.items():
            params[k] = escape(v[0])
        for k, v in data.items():
            data[k] = escape(v if type(v) == str else v[0])

        # for k,v in env.items():
        #     print k, ':', v
        # print '**' * 20
        # print env['wsgi.input'].read()
        self._params = params
        self.data = data
        self.user = None
        self.cookie = self.getCookie(env.get('HTTP_COOKIE'))
        self.path = env.get('PATH_INFO')
        self.method = env.get('REQUEST_METHOD')
        self.content_type = env.get('CONTENT_TYPE')
        self.http_accept = env.get('HTTP_ACCEPT')
        self.handle_name = '{}{}'.format(self.method, self.path).lower()


    def getCookie(self, s):
        if not s:
            return None
        cookies = {x.split('=')[0].strip(): x.split('=')[1].strip() for x in s.split(';') if x.find('=')}
        if cookies.has_key(_COOKIE_NAME):
            cookie = cookies.get(_COOKIE_NAME)
            cookie_msg = cookie.split('-')
            if len(cookie_msg) == 3:
                try:
                    if float(cookie_msg[1]) > time.time():
                        self.user_id = cookie_msg[0]
                        self.expires = cookie_msg[1]
                        self.cookie_md5 = cookie_msg[2]
                        return cookie
                except:
                    pass
        return cookies.get(_COOKIE_NAME)

    def get(self, key, default=None):
        return self._params.get(key, default)

    def params(self, **kwargs):
        # print self._params
        for k in kwargs.keys():
            kwargs[k] = self._params.get(k) if self._params.get(k) else kwargs[k]
        return kwargs if kwargs != {} else self._params

    # 返回key-value的dict:
    def input(self, **kwargs):
        # print self.data
        for k in kwargs.keys():
            kwargs[k] = self.data.get(k) if self.data.get(k) else kwargs[k]
        return kwargs if kwargs != {} else self.data

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
            'Content-Type': 'text/plain'
        }

    def set_header(self, key, value):
        self.headers[key] = value

    # 设置Cookie:
    def set_cookie(self, name, value, expires=None, path='/'):
        self.headers['Referer'] = 'http://127.0.0.1'
        self.headers['Cookie'] = '{}={}'.format(name, value)
        self.headers['Expires'] = time.strftime(GMT_FORMAT,time.localtime(float(expires)))

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

# 计算加密cookie:
def make_signed_cookie(id, password, max_age=604800, expires=None):
    expires = int(time.time() + max_age) if expires == None else expires
    L = [str(id), str(expires), hashlib.md5('%s-%s-%s-%s' % (id, password, expires, _COOKIE_KEY)).hexdigest()]
    return '-'.join(L), expires

# 中间件
class Middleware:
    interceptors = []
    def __init__(self, app):
        self.wrapped_app = app
    def __call__(self, environ, start_response):
        # logging.info('开始请求: {}'.format(environ['PATH_INFO']))
        # logging.info('开始设置Request')
        ctx.request = Request(environ)
        # logging.info('开始设置Response')
        ctx.response = Response()
        # logging.info('开始请求进入拦截器')
        # 拦截器
        is_wrap = None
        path = ctx.request.path
        next = lambda:self.wrapped_app(environ, start_response)
        # print('拦截器：进入请求 [{}]'.format(path))
        # print '{}'.format(len(self.interceptors))
        for intercept in self.interceptors:
            # print 'add interceptors: level:{}'.format(intercept.level)
            path_matched = False
            if len(intercept.absolute_paths) == 0 and len(intercept.startswith_paths) == 0:
                path_matched = True
            elif path in intercept.absolute_paths:
                path_matched = True
            else:
                for route in intercept.startswith_paths:
                    if path.startswith(route):
                        path_matched = True
            if not path_matched:
                continue

            def first_wrap(interceptor):
                return lambda:interceptor(lambda:self.wrapped_app(environ, start_response))

            def secend_wrap(interceptor, inner_intercept):
                return lambda: interceptor(inner_intercept)

            if not is_wrap:
                is_wrap = 1
                next = first_wrap(intercept)
            else:
                next = secend_wrap(intercept,next)
        for data in next():
            start_response(ctx.response.status, ctx.response.headers.items())
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

def getHTML(route, template_path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            ctx.response.headers['Content-Type'] = 'text/html'
            if hasattr(ctx.request, 'user_id') and ctx.request.user == None:
                user = User.find_first(id=ctx.request.user_id)
                if user:
                    md5 = hashlib.md5('%s-%s-%s-%s' % (
                    ctx.request.user_id, user['password'], ctx.request.expires, _COOKIE_KEY)).hexdigest()
                    if md5 == ctx.request.cookie_md5:
                        ctx.request.user = user
            data = func(*args, **kw)
            # print '=======> HTML:{}'.format(data)
            try:
                HTML = WSGIApplication.template_engine(template_path, data)
            except Exception, e:
                HTML = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <title>ERROR</title> </head> <body> <h1>页面渲染出错:</h1> {}</body> </html>'.format(e.message)
            return HTML
        wrapper.__method__ = 'GET'
        wrapper.__route__ = route
        return wrapper
    return decorator

# 定义API
def api(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            r = json.dumps(dict(status=1, data=data))
        except APIError, e:
            r = json.dumps(dict(status=0, error=e.error, data=e.data, message=e.message))
        except Exception, e:
            r = json.dumps(dict(status=0, error='internalerror', data=e.__class__.__name__, message=e.message))
        ctx.response.content_type = 'application/json'

        return r
    return _wrapper

# 定义GET:

def get(path):
    '''
        Define decorator @get('/path')
    '''

    def decorator(func):
        @api
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
        @api
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

# 定义PATCH:
def patch(path):
    def decorator(func):
        @api
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'PATCH'
        wrapper.__route__ = path
        return wrapper
    return decorator

# 定义delete:
def delete(path):
    def decorator(func):
        @api
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'DELETE'
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
    try:
        with open(static_path) as f:
            data = f.read()
    except:
        ctx.response.status = '404 ERROR'
        data = 'NOT FOUND 404'
    return data


# 定义拦截器:
def interceptor(level=10, startswith=[], absolute=[], html=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__type__ = 'interceptor'
        wrapper.level = level                  # 拦截优先级 0为最高
        wrapper.startswith_paths = startswith  # 请求url以此地址开头时拦截
        wrapper.absolute_paths = absolute      # 请求url完全匹配此地址时拦截
        wrapper.__html___ = html                    # 请求html页面时是否拦截
        return wrapper
    return decorator

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
        self.Middleware = Middleware

    # 添加一个URL定义:
    def add_url(self, func):
        if not hasattr(func, '__method__'):
            return
        key = '{}{}'.format(func.__method__, func.__route__).lower()
        if not self.urls.has_key(key):
            self.urls[key] = func
        else:
            # print 'you has double view functions:{}'.format(key)
            raise exceptions.EnvironmentError('regist url functions error')
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
        if not hasattr(func, '__type__'):
            return
        if func.__type__ == 'interceptor':
            self.Middleware.interceptors.append(func)
            self.Middleware.interceptors.sort(key=lambda f:int(f.level), reverse=True)
            # if not func.__patterns__:
            #     self.Middleware.interceptor['always'].append(func)
            # for pattern in func.__patterns__:
            #     self.Interceptor[pattern] = [func] if not self.Interceptor.has_key(pattern) else self.Interceptor[pattern].append(func)

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

    @classmethod
    def redirect(cls,url):
        ctx.response.headers['Content-Type'] = 'text/html'
        return WSGIApplication.template_engine('redirect.html', {'redirect':url})

# WSGI application
    # 返回WSGI处理函数:
    def get_wsgi_application(self):
        def wsgi(env, start_response):
            # print '======> 路由处理函数'
            # 路由处理函数 urls定义过的route访问
            route_fn_name = ctx.request.handle_name
            route_fn = self.urls.get(route_fn_name)
            # print route_fn_name
            # print route_fn
            if not route_fn and route_fn_name.startswith('get/'):
                for key, path_fn in self.urls.items():
                    if key.find('(') > 3 and key.find(')') > 5:
                        params = re.findall(key, route_fn_name)
                        if len(params) > 0:
                            route_fn = lambda :path_fn(*params)
                            break
                # print route_fn_name
                # print route_fn
            if route_fn:
                body = route_fn()
                # print body
                if body == None:
                    body = {'result': 'success'}
            # 网站资源访问（www目录）
            elif ctx.request.method == 'GET':
                body = staticFileRoute(ctx.request.path)
            else:
                ctx.response.content_type = 'application/json'
                body = json.dumps({'result': 'error','message':'no the api({}) handle function'.format(ctx.request.handle_name)})
            return [body]
        return self.Middleware(wsgi)
#WSGI server
    # 开发模式下直接启动WSGI服务器:
    def run(self, port=9000, host='127.0.0.1'):
        from wsgiref.simple_server import make_server
        server = make_server(host, port, self.get_wsgi_application())
        print('run server on {}:{}'.format(host, port))
        server.serve_forever()
        # server.handle_request() # 只能处理一次请求